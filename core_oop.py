# -*- coding: utf-8 -*-
"""
Created on 2018/9/3

Creator: cts
"""
import logging
import time

from mouse_event_api import Commands, MouseController
from special_wnds import LoginWindow, KickedWarning, SpeedMeter, MainWindow
from win_api import most_wanted_wnd, cursor_by_client, pull_2_surface, __window_rect

COMMANDS_GROUP_RELOGIN = (Commands(*KickedWarning.click_pos, extra='l'),
                          Commands(*LoginWindow.click_pos, extra='l'))
# logging setup
core_accounting = logging.getLogger(__name__)
core_accounting.setLevel(logging.DEBUG)
console_formatter = logging.Formatter('%(asctime)s||%(name)s > %(levelname)s @line_No.%(lineno)s|| %(message)s',
                                      datefmt='%H:%M:%S')

write_2_console = logging.StreamHandler()
write_2_console.setLevel(logging.INFO)
write_2_console.setFormatter(console_formatter)

core_accounting.addHandler(write_2_console)


###

class XLHelper:
    __get_wnd_rect = __window_rect

    def __init__(self):
        self.__start_time = time.time()

        self.__running_status = None
        self.__worktime_statics = None

    def __examination(self):
        pass

    def engage_process(self):
        xl_helper_mc = MouseController()
        kicked_warning_hnd = most_wanted_wnd(KickedWarning)
        login_window_hnd = most_wanted_wnd(LoginWindow)

        relogin_attempts_num = 0
        while login_window_hnd and kicked_warning_hnd:
            if relogin_attempts_num > 4:
                break
            relogin_commands_group = (
                Commands(*cursor_by_client(kicked_warning_hnd, *KickedWarning.click_pos), extra='l', delay=0.1),
                Commands(*cursor_by_client(login_window_hnd, *LoginWindow.click_pos), extra='l'))

            pull_2_surface(login_window_hnd)
            pull_2_surface(kicked_warning_hnd)
            xl_helper_mc(relogin_commands_group)

            relogin_attempts_num += 1
            core_accounting.debug("relogin at tempts number > {attempt_num}".format(attempt_num=relogin_attempts_num))

        if not got_kicked():
            core_accounting.info("Successfully relogin!")

        time.sleep(9)

        speed_meter_hnd = most_wanted_wnd(SpeedMeter)
        restart_download_commands_group = ((
                                               Commands(*cursor_by_client(speed_meter_hnd, *SpeedMeter.click_pos),
                                                        extra='r'),
                                               Commands(*cursor_by_client(speed_meter_hnd, *SpeedMeter.click_pos),
                                                        extra='free', delay=0.2),
                                               Commands(*cursor_by_client(speed_meter_hnd, *SpeedMeter.stop_pos),
                                                        extra='l', delay=0.3)) * 3)
        pull_2_surface(speed_meter_hnd)
        xl_helper_mc(restart_download_commands_group)

    def idle_process(self):
        speed_meter_hnd = most_wanted_wnd(SpeedMeter)
        if speed_meter_hnd:
            top, *_, left = __window_rect(speed_meter_hnd)
            core_accounting.debug('Nominal, speed meter pos > {speed_meter_pos}'.format(speed_meter_pos=(top, left)))
        else:
            core_accounting.debug('Cant find speed meter.')
        time.sleep(4)

    def run_forever(self):
        while True:
            if self.__examination():
                self.engage_process()
            else:
                self.idle_process()
