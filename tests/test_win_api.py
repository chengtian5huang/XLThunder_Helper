# -*- coding: utf-8 -*-
"""
Created on 2018/9/2

Creator: cts
"""


def test_win_api():
    from special_wnds import LoginWindow
    from win_api import most_wanted_wnd, pull_2_surface

    hnd = most_wanted_wnd(LoginWindow)
    pull_2_surface(hnd)
