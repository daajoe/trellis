#!/usr/bin/env false
import json
import os
from subprocess import Popen, PIPE, call
import sys

from trellis.decomposer.pace import PACEDecomposer


class Minfillbgmrs2017(PACEDecomposer):
    name = 'minfillbgmrs2017'
    bin_name = 'minfillbgmrs'
    folder_name = 'minfillmrs2017'


class Minfillmrs2017(PACEDecomposer):
    name = 'minfillmrs2017'
    bin_name = 'minfillmrs'
    folder_name = 'minfillbgmrs2017'
