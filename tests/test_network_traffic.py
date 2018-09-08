# -*- coding: utf-8 -*-
"""
Created on 2018/9/3

Creator: cts
"""
from network_traffic import avg_speed, total_traffic, total_traffic_psutil


def test_avg_test():
    for _ in range(5):
        print('{}{}'.format(*avg_speed()))


def test_total_traffic():
    interval = 10
    print('\n\n\n total traffic in {} secs > {}{}'.format(interval, *total_traffic(interval)))


def test_total_traffic_psutil():
    interval = 15
    print('\n\n\n total traffic in {} secs > {}{}'.format(interval, *total_traffic_psutil(interval)))
