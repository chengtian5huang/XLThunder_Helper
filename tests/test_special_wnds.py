# -*- coding: utf-8 -*-
"""
Created on 2018/8/31

Creator: cts
"""
import special_wnds
from mouse_event_api import MouseController, Commands
from win_api import most_wanted_wnd, cursor_by_client, pull_2_surface


def test_common_ones():
    print(hex(most_wanted_wnd(special_wnds.SpeedMeter)))
    print(hex(most_wanted_wnd(special_wnds.MainWindow)))
    print(hex(most_wanted_wnd(special_wnds.LoginWindow)))


def test_rare():
    print(hex(most_wanted_wnd(special_wnds.KickedWarning)))


def test_speed_meter_stop_pos():
    speed_meter_hnd = most_wanted_wnd(special_wnds.SpeedMeter)
    stop_download_commands_group = (
        Commands(*cursor_by_client(speed_meter_hnd, *special_wnds.SpeedMeter.click_pos),
                 extra='r'),
        Commands(*cursor_by_client(speed_meter_hnd, *special_wnds.SpeedMeter.click_pos),
                 extra='free', delay=0.1),  # this command is essential
        Commands(*cursor_by_client(speed_meter_hnd, *special_wnds.SpeedMeter.stop_pos), extra='l'),
    )
    mc = MouseController()
    mc(stop_download_commands_group)


def test_speed_meter_start_pos():
    speed_meter_hnd = most_wanted_wnd(special_wnds.SpeedMeter)
    stop_download_commands_group = (
        Commands(*cursor_by_client(speed_meter_hnd, *special_wnds.SpeedMeter.click_pos),
                 extra='r'),
        Commands(*cursor_by_client(speed_meter_hnd, *special_wnds.SpeedMeter.click_pos),
                 extra='free', delay=0.1),  # this command is essential
        Commands(*cursor_by_client(speed_meter_hnd, *special_wnds.SpeedMeter.start_pos), extra='l'),
    )
    mc = MouseController()
    mc(stop_download_commands_group)


def test_login_windos():
    login_window_hnd = most_wanted_wnd(special_wnds.LoginWindow)
    login_commands_group = (
        Commands(*cursor_by_client(login_window_hnd, *special_wnds.LoginWindow.click_pos),
                 extra='r', delay=0.2),)
    mc = MouseController()
    pull_2_surface(login_window_hnd)
    mc(login_commands_group)
