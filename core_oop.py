# -*- coding: utf-8 -*-
"""
Created on 2018/9/3

Creator: cts
"""
import logging
import time

from mouse_event_api import MouseController
from special_commands_group import restart_dl_cg, relogin_cg
from special_wnds import LoginWindow, KickedWarning, SpeedMeter, MainWindow
from win_api import most_wanted_wnd, pull_2_surface, get_window_rect, sink_2_bottom


class XLHelper:
    def __init__(self, verbose=False):
        self._start_time = time.time()
        self._is_verbose = verbose
        self._logger = self._log_conf()

        self._kicked_count = 0

        self._mouse_ctrler = MouseController()
        self._logger.info('XLHelper Start!')

    def _log_conf(self):
        core_log = logging.getLogger(self.__class__.__name__)
        core_log.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter('%(asctime)s||%(name)s > %(levelname)s @LineNo.%(lineno)s|| %(message)s',
                                              datefmt='%H:%M:%S')

        console_log = logging.StreamHandler()
        console_log.setLevel(logging.DEBUG if self._is_verbose else logging.INFO)
        console_log.setFormatter(console_formatter)
        core_log.addHandler(console_log)
        return core_log

    def _got_kicked(self):
        kicked_warning_hnd = most_wanted_wnd(KickedWarning)
        login_window_hnd = most_wanted_wnd(LoginWindow)
        result = login_window_hnd and kicked_warning_hnd

        if result:
            self._kicked_count += 1

            self._logger.debug(
                "\n\n\nGot kicked out > {kicked_warning_wnd}, {login_window_wnd}".format(
                    kicked_warning_wnd=kicked_warning_hnd,
                    login_window_wnd=login_window_hnd))
            self._logger.info('\n\nGot kicked out! Kicked Times: {0}'.format(self._kicked_count))
        return result

    def _engage_process(self):
        kicked_warning_hnd = most_wanted_wnd(KickedWarning)
        login_window_hnd = most_wanted_wnd(LoginWindow)

        relogin_attempts_num = 0
        while login_window_hnd and kicked_warning_hnd:
            if relogin_attempts_num > 4:
                break
            relogin_commands_group = relogin_cg(kicked_warning_hnd, login_window_hnd)

            pull_2_surface(login_window_hnd)
            pull_2_surface(kicked_warning_hnd)
            self._mouse_ctrler(relogin_commands_group)

            kicked_warning_hnd = most_wanted_wnd(KickedWarning)
            login_window_hnd = most_wanted_wnd(LoginWindow)
            relogin_attempts_num += 1
            self._logger.debug("relogin attempts number > {attempt_num}".format(attempt_num=relogin_attempts_num))

        if not self._got_kicked():
            self._logger.info("Successfully relogin!")

        self._sink_mainwindow()
        time.sleep(9)

        speed_meter_hnd = most_wanted_wnd(SpeedMeter)
        restart_download_commands_group = restart_dl_cg(speed_meter_hnd)
        pull_2_surface(speed_meter_hnd)
        self._mouse_ctrler(restart_download_commands_group)

        self._sink_mainwindow()
        self._logger.info("Successfully restart download!")

    def _sink_mainwindow(self):
        self._logger.debug('try sink main window')
        mainwindow_hnd = most_wanted_wnd(MainWindow)
        sink_2_bottom(mainwindow_hnd)

    def _idle_process(self):
        speed_meter_hnd = most_wanted_wnd(SpeedMeter)
        if speed_meter_hnd and self._is_verbose:
            top, *_, left = get_window_rect(speed_meter_hnd)
            self._logger.debug('Nominal, speed meter pos > {speed_meter_pos}'.format(speed_meter_pos=(top, left)))
        else:
            self._logger.debug('Cant find speed meter.')
        time.sleep(3)

    def start(self):
        while True:
            if self._got_kicked():
                self._engage_process()
            else:
                self._idle_process()


if __name__ == '__main__':
    _ = XLHelper(verbose=False)
    _.start()
