#!/usr/bin/env python
#
# Copyright 2017
# Johannes K. Fichte, TU Wien, Austria
#
# runsolver_wrapper.py is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
# runsolver_wrapper.py is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.  You should have received a
# copy of the GNU General Public License along with
# runsolver_wrapper.py.  If not, see <http://www.gnu.org/licenses/>.
import argparse
import cpuinfo
from distutils.spawn import find_executable
import json
import os
import platform
import psutil
import socket
import signal
from subprocess import Popen, PIPE, call
import sys
import tempfile
import time


def handler(signum, frame):
    current_process = psutil.Process()
    children = current_process.children(recursive=True)
    for child in children:
        sys.stderr.write('Child pid is {}\n'.format(child.pid))
        sys.stderr.write('Killing child\n')
        os.kill(child.pid, 15)
        sys.stderr.write('SIGNAL received\n')
    raise RuntimeError('signal')


def get_system_info():
    ret = {'plattform': platform.linux_distribution(), 'arch': platform.architecture(),
           'python_version': platform.python_version(), 'node': platform.node(), 'uname': platform.uname(),
           'cpu': cpuinfo.get_cpu_info(), 'libc': platform.libc_ver()}
    return ret


def parse_args(solver_bin):
    parser = argparse.ArgumentParser(description='%s -f instance')

    parser.add_argument('-f', '--file', dest='instance', action='store', type=lambda x: os.path.realpath(x),
                        help='instance', required=True)
    parser.add_argument('-b', '--binary', dest='solver', action='store', help='solver_binary', default=solver_bin)
    parser.add_argument('-W', '--wall-clock-limit', dest='timelimit', action='store', type=int, help='time-limit',
                        default=0)
    parser.add_argument('-r', '--repeat', dest='repeat', action='store', type=int, help='number of repeations',
                        default=1)
    parser.add_argument('--runid', dest='runid', action='store', type=int, help='id of the current repeation',
                        default=1)
    parser.add_argument('-t', '--tmp', dest='tmp', action='store', type=str, help='unused', default=None)
    args = parser.parse_args()
    if not os.path.isfile(args.instance):
        sys.stderr.write('File "%s" does not exist.\n\n' % args.instance)
        exit(1)
    return args


def tcs_extract_width(s):
    for line in s.split('\n'):
        line = line.split()
        if line == []:
            continue
        elif line[0] == 'c' and line[1] == 'width':
            return int(line[3].split(',')[0]), float(line[6])
    return -1, -1


# TODO:
def main():
    def debug(value):
        if args.debug:
            sys.stderr.write('%s\n' % value)

    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)

    solver_bin = 'tcs-meiji'
    args = parse_args(solver_bin)

    try:
        if os.environ.has_key('COBRA_NFSROOT') or os.environ['BATCH_SYSTEM'] == 'HTCondor':
            condor = True
    except KeyError:
        condor = False

    solver_name = os.path.basename(args.solver)
    if condor:
        home = os.path.expanduser("~")
        solver_name = os.path.join(home, 'src/treewidth-portfolio/solvers/exact/tcs-meiji/tw-exact')
    else:
        solver_name = find_executable(solver_name)

    p = Popen(['sha256sum', args.instance], stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    rc = p.returncode
    sha = output.split()[0]

    # prepare solver call
    call = '%s < %s' % (solver_name, args.instance)
    sys.stderr.write(''.join(call))
    sys.stderr.write('\n')

    wallstart = time.time()
    wallmin = sys.maxint
    wallmax = wall = 0
    iwidth = (sys.maxint, None)
    solved = True
    err = ''
    try:
        for i in xrange(args.repeat):
            lwallstart = time.time()
            p = Popen(call, stdout=PIPE, stderr=PIPE, shell=True)
            output, err = p.communicate()
            lwall = time.time() - lwallstart
            wallmin = min(lwall, wallmin)
            wallmax = max(lwall, wallmax)
            rc = p.returncode
            res = tcs_extract_width(output)
            iwidth = min(res, iwidth, key=lambda x: x[0])
        wall = time.time() - wallstart
    except RuntimeError as e:
        err = e
        solved = False

    res = {'instance': args.instance, 'retcode': rc, 'width': iwidth[0], 'sruntim': iwidth[1], 'wall': wall,
           'wallmax': wallmax, 'wallmin': wallmin, 'solver': solver_name, 'hash': sha, 'call': call,
           'args': vars(args), 'solved': solved, 'err': err, 'system_info': get_system_info(),
           'run': args.runid}
    sys.stdout.write(json.dumps(res, sort_keys=True))
    sys.stdout.write('\n')


if __name__ == "__main__":
    main()
