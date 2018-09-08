# -*- coding: utf-8 -*-
"""
Created on 2018/9/2

Creator: cts
"""
import math
import time

from win_api import __user32lib

from mouse_event_api import Commands, MouseController, normalize_coord

SCREEN_CENTER = __user32lib.GetSystemMetrics(0) / 2, __user32lib.GetSystemMetrics(1) / 2


def circle_coords(a, b, radius, steps=36):
    for step in range(steps + 1):
        circle_point_x, circle_poine_y = a + radius * math.cos(step * 2 * math.pi / steps), b + radius * math.sin(
            step * 2 * math.pi / steps)
        yield circle_point_x, circle_poine_y


def test_command_controller():
    circle_cmds_group = (Commands(x=circle_x, y=circle_y, extra='') for circle_x, circle_y in
                         circle_coords(*SCREEN_CENTER, 200, steps=30))
    mc = MouseController()
    mc(circle_cmds_group)


def test_draging_cursor():
    circle_cmds_group = (Commands(x=circle_x, y=circle_y, extra='L', delay=0.01) for circle_x, circle_y in
                         circle_coords(*SCREEN_CENTER, 200, steps=180))
    mc = MouseController()
    time.sleep(3)
    mc(circle_cmds_group)


def test_release_buttons():
    from mouse_event_api import _release_mouse_buttons
    _release_mouse_buttons(*normalize_coord(*SCREEN_CENTER))
