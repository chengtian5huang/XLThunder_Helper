# -*- coding: utf-8 -*-
"""
Created on 2018/9/1

Creator: cts
"""
import ctypes


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long),
                ("y", ctypes.c_long)]
