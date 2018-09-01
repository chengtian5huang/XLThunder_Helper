# -*- coding: utf-8 -*-
"""
Created on 2018/9/1

Creator: cts
"""
import ctypes
import pprint
import re
from typing import NamedTuple


class StructDef2Ctypes:
    template = """class {class_name}(ctypes.Structure):
    _fields_ = {fields_list}"""
    c_type_convert_table = {
        "LONG": ctypes.c_long,
        "DWORD": ctypes.c_double,
        "ULONG_PTR": ctypes.c_ulong,
        "WORD": ctypes.c_ulong
    }

    class __BuiltStruct(NamedTuple):
        name: str = ""
        fields: list = list()

    def __init__(self):
        self.__build_group = list()
        self.__code = None
        self.__struct_area = re.compile(r"(?P<struct_name>\w+)\s+{\n(?P<fields>[\s\w;_]+)\n}+")
        self.__type_n_field = re.compile(r"(?P<one_field>(?P<c_type>\w+)\s+(?P<field_name>\w+);)+")
        self.__c_type_pattern = re.compile(r"<class '(?P<pure_name>[\w.]+)'>")

    def __code_post_effect(self):
        def pure_type_name(match_obj):
            return match_obj.group("pure_name")

        self.__code = re.sub(self.__c_type_pattern, pure_type_name, self.__code)

    def code(self, text):
        self.parse(text)
        self.__code = "\n\n".join(self.template.format(class_name=one_struct.name,
                                                       fields_list=pprint.pformat(one_struct.fields, indent=0))
                                  for one_struct in self.__build_group)
        self.__code_post_effect()
        return self.__code

    def parse(self, text):
        built_structs = list()
        for one_struct_area in re.finditer(self.__struct_area, text):
            building_class_name = one_struct_area.group("struct_name")
            building_class_fields = one_struct_area.group("fields")
            building_class = type(building_class_name,
                                  (ctypes.Structure,), dict())

            # attach fields for new struct just built above.
            tmp_fields = list()
            for one_field in re.finditer(self.__type_n_field, building_class_fields):
                this_name = one_field.group("field_name")
                this_type = self.c_type_convert_table[one_field.group("c_type")]
                tmp_fields.append((this_name, this_type))
            building_class._fields_ = tmp_fields

            # done building one struct.
            built_structs.append(building_class)

            # store information for generate code.
            tmp_builtstruct = self.__BuiltStruct._make((building_class_name, tmp_fields))
            self.__build_group.append(tmp_builtstruct)
        return built_structs

    def __call__(self, text):
        return self.parse(text)
