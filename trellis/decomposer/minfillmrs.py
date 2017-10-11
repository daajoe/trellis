#!/usr/bin/env false

from trellis.decomposer.pace import PACEDecomposer


class Minfillbgmrs2017(PACEDecomposer):
    name = 'minfillbgmrs2017'
    bin_name = 'minfillbgmrs'
    folder_name = 'minfillmrs2017'
    is_heuristic = True


class Minfillmrs2017(PACEDecomposer):
    name = 'minfillmrs2017'
    bin_name = 'minfillmrs'
    folder_name = 'minfillmrs2017'
    is_heuristic = True
