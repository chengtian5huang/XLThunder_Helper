# -*- coding: utf-8 -*-
"""
Created on 2018/9/7

Creator: cts
"""
from mouse_event_api import Commands
from special_wnds import SpeedMeter, KickedWarning, LoginWindow
from win_api import cursor_by_client


def stop_dl_cg(hnd):
    return ((
                Commands(*cursor_by_client(hnd, *SpeedMeter.click_pos),
                         extra='r'),
                Commands(*cursor_by_client(hnd, *SpeedMeter.click_pos),
                         extra='free', delay=0.2),  # this command is essential
                Commands(*cursor_by_client(hnd, *SpeedMeter.stop_pos), extra='l', delay=0.3),
            ) * 3)


def restart_dl_cg(hnd):
    return ((
                Commands(
                    *cursor_by_client(hnd, *SpeedMeter.click_pos),
                    extra='r'),
                Commands(
                    *cursor_by_client(hnd, *SpeedMeter.click_pos),
                    extra='free', delay=0.2),  # this command is essential
                Commands(
                    *cursor_by_client(hnd, *SpeedMeter.start_pos),
                    extra='l', delay=0.3),
            ) * 3)


def relogin_cg(kw_hnd, lw_hnd):
    return (
        Commands(*cursor_by_client(kw_hnd, *KickedWarning.click_pos), extra='l', delay=0.1),
        Commands(*cursor_by_client(lw_hnd, *LoginWindow.click_pos), extra='l'))
