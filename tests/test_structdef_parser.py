# -*- coding: utf-8 -*-
"""
Created on 2018/9/1

Creator: cts
"""


def test_building_class():
    example_text = """typedef struct tagHARDWAREINPUT {
  DWORD uMsg;
  WORD  wParamL;
  WORD  wParamH;
} HARDWAREINPUT, *PHARDWAREINPUT, *LPHARDWAREINPUT;
typedef struct tagMOUSEINPUT {
  LONG      dx;
  LONG      dy;
  DWORD     mouseData;
  DWORD     dwFlags;
  DWORD     time;
  ULONG_PTR dwExtraInfo;
} MOUSEINPUT, *PMOUSEINPUT, *LPMOUSEINPUT;"""
    from aux_cstruct_parser import cstruct_parser
    parser = cstruct_parser.StructDef2Ctypes()
    _ = parser(example_text)
    pass


def test_usage():
    example_text = """typedef struct _RECT {
  LONG left;
  LONG top;
  LONG right;
  LONG bottom;
} RECT, *PRECT;"""
    from aux_cstruct_parser import cstruct_parser
    parser = cstruct_parser.StructDef2Ctypes()
    parse_result = parser(example_text)
    assert 1 == len(parse_result)
    assert "RECT" in parse_result[0].__name__
    built_class = parse_result[0]
    rect = built_class()

    import special_wnds
    import ctypes
    from win_api import most_wanted_wnd, __user32lib
    hnd = most_wanted_wnd(special_wnds.SpeedMeter)

    assert 1 == __user32lib.GetWindowRect(hnd, ctypes.byref(rect))
    assert 150 == rect.right - rect.left == rect.bottom - rect.top
    print("\n", rect.left, rect.top, rect.right, rect.bottom)


def test_output_code():
    example_text = """typedef struct tagHARDWAREINPUT {
  DWORD uMsg;
  WORD  wParamL;
  WORD  wParamH;
} HARDWAREINPUT, *PHARDWAREINPUT, *LPHARDWAREINPUT;
typedef struct tagMOUSEINPUT {
  LONG      dx;
  LONG      dy;
  DWORD     mouseData;
  DWORD     dwFlags;
  DWORD     time;
  ULONG_PTR dwExtraInfo;
} MOUSEINPUT, *PMOUSEINPUT, *LPMOUSEINPUT;
typedef struct _RECT {
  LONG left;
  LONG top;
  LONG right;
  LONG bottom;
} RECT, *PRECT;"""
    from aux_cstruct_parser import cstruct_parser
    parser = cstruct_parser.StructDef2Ctypes()
    # print("\n", parser.code(example_text))
    answer = """class tagHARDWAREINPUT(ctypes.Structure):
    _fields_ = [('uMsg', ctypes.c_double),
('wParamL', ctypes.c_ulong),
('wParamH', ctypes.c_ulong)]

class tagMOUSEINPUT(ctypes.Structure):
    _fields_ = [('dx', ctypes.c_long),
('dy', ctypes.c_long),
('mouseData', ctypes.c_double),
('dwFlags', ctypes.c_double),
('time', ctypes.c_double),
('dwExtraInfo', ctypes.c_ulong)]

class _RECT(ctypes.Structure):
    _fields_ = [('left', ctypes.c_long),
('top', ctypes.c_long),
('right', ctypes.c_long),
('bottom', ctypes.c_long)]"""
    assert answer == parser.code(example_text)
