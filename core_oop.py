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
    def __init__(self):
        self._start_time = time.time()