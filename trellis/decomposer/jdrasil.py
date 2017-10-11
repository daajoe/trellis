#!/usr/bin/env false
from trellis.decomposer.pace import PACEDecomposer


class Jdrasil2016(PACEDecomposer):
    name = 'jdrasil2016'
    bin_name = 'jdrasil'
    folder_name = 'jdrasil2016'

    args = ['-log -e PBLib_incremental', '-log -e commander', '-log -e PBLib']


class Jdrasil2017(PACEDecomposer):
    name = 'jdrasil2017'
    bin_name = 'jdrasil'
    folder_name = 'jdrasil2017'

    args = ['-log -e PBLib_incremental', '-log -e commander', '-log -e PBLib']


class JdrasilHeuristic2017(PACEDecomposer):
    name = 'jdrasil2017'
    bin_name = 'jdrasil'
    folder_name = 'jdrasil2017'
    is_heuristic = True

    args = ['-log -heuristic -e PBLib_incremental', '-log -heuristic -e commander', '-log -heuristic -e PBLib']
