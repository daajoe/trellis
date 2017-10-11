#!/usr/bin/env false
import json
from subprocess import Popen, PIPE, call
import sys

from trellis.decomposer.pace import PACEDecomposer


class FlowCutter2016(PACEDecomposer):
    name = 'flowcutter2016'
    bin_name = 'flowcutter'
    folder_name = 'flowcutter2016'


class FlowCutter2017(PACEDecomposer):
    name = 'flowcutter2017'
    bin_name = 'flowcutter'
    folder_name = 'flowcutter2017'