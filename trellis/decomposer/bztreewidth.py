#!/usr/bin/env false
import json
from subprocess import Popen, PIPE, call
import sys

import os

from trellis.decomposer.pace import PACEDecomposer


# TODO:
class BzTreewidth2016(PACEDecomposer):
    name = 'BZTreewidth-%s.exe'
    bin_name = 'BZTreewidth-%s.exe'
    folder_name = 'bztreewidth2016'

    args = ['DFS', 'DFS-LS', 'DFS-SV-ASV-EADD-MMW', 'DFS-SV-ASV-MMW', 'DFS-SV', 'DFS-SV-ASV-MMWLIMIT',
            'BZTreewidth-DFS-SV-MMWLIMIT', 'BZTreewidth-DFS-SV-MMW', 'DP', 'DP-LS']

    def call_solver(self, instance_path, timeout=30, iterations=None):
        print 'args:', self.args
        if '%s' in self.name:
            self.name = self.name % self.args
        if '%s' in self.bin_name:
            self.bin_name = self.bin_name % self.args
        print self.name
        path = os.path.join(self.lib_path, self.folder_name, self.bin_name)
        cmd = 'timeout %i %s < %s' % (timeout, path, instance_path)
        return self.call(cmd)
