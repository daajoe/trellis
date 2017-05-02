#!/usr/bin/env python
import json
from subprocess import Popen, PIPE, call
import sys

def compute_ordering_htd(file_name,graph,path,iterations=100):
    #ret=call(cmd_make, shell=True)
    
    cmd='%s --iterations %i --opt width --output width --input gr --strategy challenge < %s' % ('htd_main',iterations,file_name)

    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True, cwd=path)
    output, err = p.communicate()
    sys.stderr.write(err)
    ret=json.loads(output)
    return ret
