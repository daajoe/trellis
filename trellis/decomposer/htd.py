#!/usr/bin/env false
import json
import os
from subprocess import Popen, PIPE, call
import sys

from trellis.decomposer.pace import PACEDecomposer


class HTD(PACEDecomposer):
    name = 'htd'
    bin_name = 'htd'
    folder_name = 'htd'

    #TODO: allow varying strategy
    # min-fill          Minimum fill ordering algorithm (default)
    # min-degree        Minimum degree ordering algorithm
    # max-cardinality   Maximum cardinality search ordering algorithm
    # challenge
    # min-degree

    def call_solver(self, instance_path, timeout=30, iterations=100):
        path = os.path.join(self.lib_path, self.folder_name, self.bin_name)
        cmd = 'timeout %i %s --iterations %i --opt width --output td --input gr --strategy challenge < %s' \
              % (timeout, path, iterations, instance_path)
        return self.call(cmd)
