#!/usr/bin/env false
import os

from trellis.decomposer.pace import PACEDecomposer


class HTD2016(PACEDecomposer):
    name = 'htd2016'
    bin_name = 'htd'
    folder_name = 'htd2016'

    # TODO: allow varying strategy
    # TODO: expose seed
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


class HTD2017(HTD2016):
    name = 'htd2017'
    bin_name = 'htd'
    folder_name = 'htd2017'
