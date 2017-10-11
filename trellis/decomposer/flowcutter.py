#!/usr/bin/env false
import json
from subprocess import Popen, PIPE, call
import sys

from trellis.decomposer.pace import PACEDecomposer


# TODO:
class FlowCutter(PACEDecomposer):
    name = 'fc'
    path = 'flow_cutter'

    # TODO: allow varying strategy
    # min-fill          Minimum fill ordering algorithm (default)
    # min-degree        Minimum degree ordering algorithm
    # max-cardinality   Maximum cardinality search ordering algorithm
    # challenge
    # min-degree

    def call_solver(self, instance_path, timeout=30, iterations=None):
        raise NotImplementedError
        cmd = 'timeout %s %s < %s' % (timeout, self.path, instance_path)
        return self.call(cmd)
