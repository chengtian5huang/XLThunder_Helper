# -*- coding: utf-8 -*-
"""
Created on 2018/8/31

Creator: cts
"""
import ctypes

import c_types

__user32lib = ctypes.WinDLL(r"C:\Windows\System32\user32.dll")


def find_wnd(classname, title):
    game = __user32lib.FindWindowW(classname, title)
    if game == 0:
        raise LookupError
    else:
        return game


def most_wanted_wnd(wanted):
    return find_wnd(wanted.classname, wanted.title)


def most_wanted_cursor_pos(wanted):
    wanted_hnd = most_wanted_wnd(wanted)
    return cursor_by_client(wanted_hnd, *wanted.click_pos)


def cursor_by_client(hnd, x, y):
    apoint = c_types.ScreenPoint()
    apoint.x, apoint.y = x, y
    __user32lib.ClientToScreen(int(hnd), ctypes.byref(apoint))
    return apoint.x, apoint.y
