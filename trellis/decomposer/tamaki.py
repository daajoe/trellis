#!/usr/bin/env false

from trellis.decomposer.pace import PACEDecomposer


class Tamaki2016(PACEDecomposer):
    name = 'tamaki2016'
    bin_name = 'tamaki'
    folder_name = 'tamaki2016'


class Tamaki2017(PACEDecomposer):
    name = 'tamaki2017'
    bin_name = 'tamaki-exact'
    folder_name = 'tamaki2017'


class TamakiHeuristic2017(PACEDecomposer):
    name = 'tamaki2017'
    bin_name = 'tamaki-heuristic '
    folder_name = 'tamaki2017'
