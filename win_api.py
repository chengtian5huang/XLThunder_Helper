# -*- coding: utf-8 -*-
"""
Created on 2018/8/31

Creator: cts
"""
import ctypes
import c_types

__user32lib = ctypes.WinDLL(r"C:\Windows\System32\user32.dll")


class RECT(ctypes.Structure):
    """ creates a struct to match emxArray_real_T """

    _fields_ = [('left', ctypes.c_int),
                ('right', ctypes.c_int),
                ('top', ctypes.c_int),
                ('bottom', ctypes.c_int)]


def find_wnd(classname, title):
    game = __user32lib.FindWindowW(classname, title)
    if game == 0:
        return False
    return game


def most_wanted_wnd(wanted):
    return find_wnd(wanted.classname, wanted.title)


def most_wanted_cursor_pos(wanted):
    wanted_hnd = most_wanted_wnd(wanted)
    return cursor_by_client(wanted_hnd, *wanted.click_pos)


def cursor_by_client(hnd, x, y):
    apoint = c_types.ScreenPoint()
    apoint.x, apoint.y = x, y
    __user32lib.ClientToScreen(int(hnd), ctypes.byref(apoint))
    return apoint.x, apoint.y


def __window_rect(hnd):
    tmp_rect = RECT()
    __user32lib.GetWindowRect(hnd, ctypes.byref(tmp_rect))
    return tmp_rect.top, tmp_rect.right, tmp_rect.bottom, tmp_rect.left


def pull_2_surface(hnd):
    top, right, bottom, left = __window_rect(hnd)
    wnd_width, wnd_height = right - left, bottom - top
    __user32lib.SetWindowPos(hnd, 0, 0, 0, 0, 0, 0x0443)
