#!/usr/bin/env python
# coding=utf-8
import psutil
import signal, os, sys


class AbortException(Exception):
    pass


class TimeoutException(AbortException):
    pass


class InterruptException(AbortException):
    pass


def handler(signum, frame):
    sys.stderr.write('signum %s' % signum)
    current_process = psutil.Process()
    children = current_process.children(recursive=True)
    for child in children:
        sys.stderr.write('Child pid is {}\n'.format(child.pid))
        sys.stderr.write('Killing child\n')
        try:
            os.kill(child.pid, 15)
        except OSError, e:
            sys.stderr.write('Process might already be gone. See error below.\n')
            sys.stderr.write('%s' % str(e))

    sys.stderr.write('SIGNAL received\n')
    if signum == 15:
        raise TimeoutException('signal')
    else:
        raise InterruptException('signal')


def nothing(signum, frame):
    current_process = psutil.Process()
    children = current_process.children(recursive=True)
    for child in children:
        sys.stderr.write('Child pid is {}\n'.format(child.pid))
        sys.stderr.write('Killing child\n')
        try:
            os.kill(child.pid, 15)
        except OSError, e:
            sys.stderr.write('Process might already be gone. See error below.\n')
            sys.stderr.write('%s' % str(e))
    sys.stderr.write('SIGNAL received\n')
