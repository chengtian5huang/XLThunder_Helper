# -*- coding: utf-8 -*-
"""
Created on 2018/8/31

Creator: cts
"""
import time

import special_wnds
from mouse_event_api import MouseController, Commands
from special_commands_group import restart_dl_cg
from win_api import most_wanted_wnd, cursor_by_client, pull_2_surface, sink_2_bottom


def test_common_ones():
    print(hex(most_wanted_wnd(special_wnds.SpeedMeter)))
    print(hex(most_wanted_wnd(special_wnds.MainWindow)))
    print(hex(most_wanted_wnd(special_wnds.LoginWindow)))


def test_rare():
    hnd = most_wanted_wnd(special_wnds.KickedWarning)
    assert hnd
    print(hex(hnd))


def test_speed_meter_stop_pos():
    speed_meter_hnd = most_wanted_wnd(special_wnds.SpeedMeter)
    stop_download_commands_group = restart_dl_cg(speed_meter_hnd)
    mc = MouseController()
    mc(stop_download_commands_group)


def test_speed_meter_start_pos():
    speed_meter_hnd = most_wanted_wnd(special_wnds.SpeedMeter)
    stop_download_commands_group = restart_dl_cg(speed_meter_hnd)
    mc = MouseController()
    mc(stop_download_commands_group)


def test_login_windos():
    login_window_hnd = most_wanted_wnd(special_wnds.LoginWindow)
    mc = MouseController()
    login_commands_group = (
        Commands(*cursor_by_client(login_window_hnd, *special_wnds.LoginWindow.click_pos),
                 extra='l', delay=0.2),)

    pull_2_surface(login_window_hnd)
    mc(login_commands_group)


def test_sink_main_window():
    time.sleep(3)
    main_window_hnd = most_wanted_wnd(special_wnds.MainWindow)
    sink_2_bottom(main_window_hnd)
