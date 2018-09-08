# -*- coding: utf-8 -*-
"""
Created on 2018/8/31

Creator: cts
"""


class SpeedMeter:
    classname: str = "XLUEFrameHostWnd"
    title: str = ""
    click_pos: tuple = (75, 75)
    stop_pos: tuple = (100, 170)
    start_pos: tuple = (100, 150)


class KickedWarning:
    classname: str = "XLUEModalHostWnd"
    title: str = "MessageBox"
    click_pos: tuple = (360, 180)


class MainWindow:
    classname: str = "XLUEFrameHostWnd"
    title: str = "迅雷U享版"


class LoginWindow:
    classname: str = "XLUEFrameHostWnd"
    title: str = "登录迅雷U享版"
    click_pos: tuple = (800, 385)
