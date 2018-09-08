# -*- coding: utf-8 -*-
"""
Created on 2018/9/2

Creator: cts
"""
import logging
import math
import time

from win_api import __user32lib
import ctypes

LONG = ctypes.c_long
DWORD = ctypes.c_ulong
ULONG_PTR = ctypes.POINTER(DWORD)
WORD = ctypes.c_ushort

STRUCT = ctypes.Structure
UNION = ctypes.Union

# logging setup
book_keeper = logging.getLogger(__name__)
book_keeper.setLevel(logging.DEBUG)
console_formatter = logging.Formatter('%(asctime)s||%(name)s > %(levelname)s @line_No.%(lineno)s|| %(message)s',
                                      datefmt='%H:%M:%S')

write_2_console = logging.StreamHandler()
write_2_console.setLevel(logging.DEBUG)
write_2_console.setFormatter(console_formatter)

book_keeper.addHandler(write_2_console)


###

class tagMOUSEINPUT(STRUCT):
    _fields_ = (('dx', LONG),
                ('dy', LONG),
                ('mouseData', DWORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))


class tagKEYBDINPUT(STRUCT):
    _fields_ = (('wVk', WORD),
                ('wScan', WORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))


class tagHARDWAREINPUT(STRUCT):
    _fields_ = (('uMsg', DWORD),
                ('wParamL', WORD),
                ('wParamH', WORD))


class Union_tagINPUT(UNION):
    _fields_ = (('mi', tagMOUSEINPUT),
                ('ki', tagKEYBDINPUT),
                ('hi', tagHARDWAREINPUT))


class tagINPUT(STRUCT):
    _fields_ = (('type', DWORD),
                ('dummy_union', Union_tagINPUT))


# see https://docs.microsoft.com/en-us/windows/desktop/api/winuser/ns-winuser-tagmouseinput#members for details.
# mouseData for tagMOUSEINPUT struct
WHEEL_DELTA = 120
XBUTTON1 = 0x0001
XBUTTON2 = 0x0002

# dwFlags for tagMOUSEINPUT struct
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_HWHEEL = 0x01000
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_MOVE_NOCOALESCE = 0x2000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_VIRTUALDESK = 0x4000
MOUSEEVENTF_WHEEL = 0x0800
MOUSEEVENTF_XDOWN = 0x0080
MOUSEEVENTF_XUP = 0x0100

# type for tagINPUT struct
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2


def make_mouse_input(data, flags, x, y):
    x, y = int(x), int(y)
    return tagINPUT(INPUT_MOUSE, Union_tagINPUT(mi=tagMOUSEINPUT(x, y, data, flags, 0, None)))


def send_input(*inputs):
    n_inputs = len(inputs)
    lpointer_input = tagINPUT * n_inputs
    pointer_inputs = lpointer_input(*inputs)
    cb_size = ctypes.c_int(ctypes.sizeof(tagINPUT))
    return __user32lib.SendInput(n_inputs, pointer_inputs, cb_size)


def normalize_coord(x, y):
    screen_xsize, screen_ysize = __user32lib.GetSystemMetrics(0), __user32lib.GetSystemMetrics(1)
    return int((x / screen_xsize) * 65535), int((y / screen_ysize) * 65535)


def _simply_move(x, y):
    send_input(make_mouse_input(XBUTTON1, 0x8001, x, y))


def _left_click(x, y):
    send_input(make_mouse_input(XBUTTON1, 0x8007, x, y))


def _right_click(x, y):
    send_input(make_mouse_input(XBUTTON1, 0x8019, x, y))


def _left_drag(x, y):
    send_input(make_mouse_input(XBUTTON1, 0x8003, x, y))


def _release_mouse_buttons(x, y):
    send_input(make_mouse_input(0, 0x8001, x, y))


class Commands:
    def __init__(self, x, y, extra, delay=0):
        self.x, self.y = int(x), int(y)
        self.normalized_x, self.normalized_y = normalize_coord(x, y)
        self.extra = extra
        self.delay = delay


class MouseController:
    MOUSE_MOVE_SIGNALS = {
        '': _simply_move,
        "l": _left_click,
        "r": _right_click,
        'L': _left_drag,
        'free': _release_mouse_buttons,
    }

    def __init__(self):
        self.lib = ctypes.WinDLL(r"C:\Windows\System32\user32.dll")
        self.__continue_zone = 100
        self.__breakout_tolerance = 2
        self.__breakout_record = 0
        self.__commands_completed = 0
        self.__current_command = None

    def __command_instructor(self):
        engagement = self.MOUSE_MOVE_SIGNALS.get(self.__current_command.extra)
        engagement(self.__current_command.normalized_x, self.__current_command.normalized_y)

        book_keeper.debug('move cursor > {curr_cmd} with extra > {curr_extra}'.format(
            curr_cmd=(self.__current_command.x, self.__current_command.y),
            curr_extra=engagement.__name__))

        in_boundary, curr_pos, distance = self.__within_boundary()
        while not in_boundary:
            self.__breakout_record += 1
            book_keeper.debug("cursor did not moved as expected!")
            book_keeper.debug(
                "actual pos > {actual_pos} vs expected pos > {expected_pos} distance: {_distance:.2f}".format(
                    actual_pos=curr_pos, expected_pos=(self.__current_command.x, self.__current_command.y),
                    _distance=distance))
            book_keeper.debug(
                'retry > {tried}/{limit}'.format(tried=self.__breakout_record, limit=self.__breakout_tolerance))
            engagement(self.__current_command.normalized_x, self.__current_command.normalized_y)

            if self.__breakout_record > self.__breakout_tolerance:
                return
        self.__commands_completed += 1

    def __current_cursor(self):
        from ctype_structures import POINT
        tmp_point = POINT()
        self.lib.GetCursorPos(ctypes.byref(tmp_point))
        return tmp_point.x, tmp_point.y

    @staticmethod
    def __distance(x1, y1, x2, y2):
        return math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)

    def __within_boundary(self):
        current_cursor = self.__current_cursor()
        distance = self.__distance(*current_cursor, self.__current_command.x, self.__current_command.y)
        in_continue_zone = distance < self.__continue_zone

        return in_continue_zone, current_cursor, distance

    def __call__(self, cmd, *cmds):
        if cmds:
            _ = list(cmds)
            _.insert(0, cmd)
            commands = _
        else:
            try:
                commands = list(cmd)
            except TypeError:
                commands = list((cmd,))
        commands.append(Commands(*self.__current_cursor(), extra='free'))  # release all button after all

        for cmd in commands:
            if self.__breakout_record > self.__breakout_tolerance:
                book_keeper.warning("Halt! User interrupts for too many times!")
                return
            self.__current_command = cmd
            self.__command_instructor()

            # maybe need to free all buttons here.

            time.sleep(self.__current_command.delay)
        book_keeper.info(
            "Successfully Complete {commands_group} Commands!".format(commands_group=self.__commands_completed))
