# -*- coding: utf-8 -*-
"""
Created on 2018/9/1

Creator: cts
"""
import ctypes


class ScreenPoint(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]
