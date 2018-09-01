# -*- coding: utf-8 -*-
"""
Created on 2018/8/31

Creator: cts
"""
import special_wnds
from win_api import most_wanted_wnd


def test_common_ones():
    print(hex(most_wanted_wnd(special_wnds.SpeedMeter())))
    print(hex(most_wanted_wnd(special_wnds.MainWindow())))
    print(hex(most_wanted_wnd(special_wnds.LoginWindow())))


def test_rare():
    print(hex(most_wanted_wnd(special_wnds.KickedWarning())))
