# -*- coding: utf-8 -*-
"""
Created on 2018/9/2

Creator: cts
"""
from time import sleep


def test_pull_2_surface():
    from special_wnds import LoginWindow
    from win_api import most_wanted_wnd, pull_2_surface

    hnd = most_wanted_wnd(LoginWindow)
    pull_2_surface(hnd)


def test_sink():
    from special_wnds import MainWindow
    from win_api import most_wanted_wnd
    from win_api import sink_2_bottom

    hnd = most_wanted_wnd(MainWindow)
    sleep(2)
    sink_2_bottom(hnd)
