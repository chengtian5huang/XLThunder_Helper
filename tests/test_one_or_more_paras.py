# -*- coding: utf-8 -*-
"""
Created on 2018/9/7

Creator: cts
"""


def f(cmd, *cmds):
    if cmds:
        _ = list(cmds)
        _.insert(0, cmd)
        cmd_group = _
    else:
        try:
            cmd_group = list(cmd)
        except TypeError:
            cmd_group = list((cmd,))
    print(cmd_group)
    return cmd_group


def test_i():
    assert 5 == len(f(5, 6, 7, 8, 8))
    assert 5 == len(f([5, 6, 7, 8, 8]))
    assert 1 == len(f(5))
