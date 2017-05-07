#!/usr/bin/env false
import json
from subprocess import Popen, PIPE, call
import sys

from trellis.decomposer.pace import PACEDecomposer


class HTD(PACEDecomposer):
    name = 'htd'
    path = 'htd_main'

    #TODO: allow varying strategy
    # min-fill          Minimum fill ordering algorithm (default)
    # min-degree        Minimum degree ordering algorithm
    # max-cardinality   Maximum cardinality search ordering algorithm
    # challenge
    # min-degree

    def call_solver(self, instance_path, timeout=30, iterations=100):
        cmd = 'timeout %i %s --iterations %i --opt width --output td --input gr --strategy challenge < %s' \
              % (timeout, self.path, iterations, instance_path)
        return self.call(cmd)
