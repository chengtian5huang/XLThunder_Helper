# -*- coding: utf-8 -*-
"""
Created on 2018/9/3

Creator: cts
"""
import logging
import subprocess
import time
from collections import namedtuple
import math

# logging setup
traffic_accounting = logging.getLogger(__name__)
traffic_accounting.setLevel(logging.DEBUG)
console_formatter = logging.Formatter('%(asctime)s||%(name)s > %(levelname)s @line_No.%(lineno)s|| %(message)s',
                                      datefmt='%H:%M:%S')

write_2_console = logging.StreamHandler()
write_2_console.setLevel(logging.DEBUG)
write_2_console.setFormatter(console_formatter)

traffic_accounting.addHandler(write_2_console)

###


TrafficReport = namedtuple('TrafficReport', ['bytes_sent', 'bytes_recv'])
unit_convert_table = ['B', 'KB', 'MB', 'GB', 'TB']


def unit_convert(num):
    i = 1024
    power = int(math.log(num, i))
    return round(num / i ** power, 3), unit_convert_table[power]


def __traffic_report():
    network_traffic = subprocess.run(['netstat', '-e'], stdout=subprocess.PIPE).stdout
    raw_report = [line.strip() for line in network_traffic.decode('gbk').split('\n') if len(line) > 20][1:-1]
    traffic_report = TrafficReport(
        *map(int, [piece for piece in raw_report[0].split(' ') if piece is not ''][::-1][:-1]))

    return traffic_report


def avg_speed(interval=2):
    recv_before = __traffic_report().bytes_recv
    time.sleep(interval)
    recv_after = __traffic_report().bytes_recv
    ans = (recv_after - recv_before) / interval

    return unit_convert(ans)


def total_traffic(interval=3):
    recv_before = __traffic_report().bytes_recv
    time.sleep(interval)
    recv_after = __traffic_report().bytes_recv
    ans = recv_after - recv_before

    traffic_accounting.debug('{before} - {after} = {_ans}'.format(before=recv_before, after=recv_after, _ans=ans))

    return unit_convert(ans)


def total_traffic_psutil(interval=3):
    import psutil
    recv_before = psutil.net_io_counters().bytes_recv
    time.sleep(interval)
    recv_after = psutil.net_io_counters().bytes_recv
    ans = recv_after - recv_before

    traffic_accounting.debug('{after} - {before} = {_ans}'.format(before=recv_before, after=recv_after, _ans=ans))

    return unit_convert(ans)
    pass
