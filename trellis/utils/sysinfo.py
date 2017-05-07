#!/usr/bin/env false
# coding=utf-8

import cpuinfo
import platform


def get_system_info():
    ret = {}
    ret['plattform'] = platform.linux_distribution()
    ret['arch'] = platform.architecture()
    ret['python_version'] = platform.python_version()
    ret['node'] = platform.node()
    ret['uname'] = platform.uname()
    ret['cpu'] = cpuinfo.get_cpu_info()
    ret['libc'] = platform.libc_ver()
    return ret
