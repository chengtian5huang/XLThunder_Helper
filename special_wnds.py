# -*- coding: utf-8 -*-
"""
Created on 2018/8/31

Creator: cts
"""
from typing import NamedTuple


class SpeedMeter(NamedTuple):
    classname: str = "XLUEFrameHostWnd"
    title: str = ""
    click_pos: tuple = (75, 75)


class KickedWarning(NamedTuple):
    classname: str = "XLUEModelHostWnd"
    title: str = "MessageBox"
    click_pos: tuple = (360, 180)


class MainWindow(NamedTuple):
    classname: str = "XLUEFrameHostWnd"
    title: str = "迅雷U享版"


class LoginWindow(NamedTuple):
    classname: str = "XLUEFrameHostWnd"
    title: str = "登录迅雷U享版"
    click_pos: tuple = (800, 300)


class PosSpeedMeter(NamedTuple):
    x: int = 75
    y: int = 75


class PosKickedWarning(NamedTuple):
    x: int = 360
    y: int = 180


class PosLoginWindow(NamedTuple):
    x: int = 800
    y: int = 380
