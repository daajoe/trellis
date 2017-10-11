#!/usr/bin/env python2.7
# encoding: utf-8

'''
trellisWrapper -- 

@author:     Johannes K. Fichte
@license:    GPL

example call (in aclib folder structure):
python smac/trellisWrapper.py --runsolver-path runsolver -- instance.dgf
'''

from genericWrapper import AbstractWrapper
import os

class SatWrapper(AbstractWrapper):
    '''
        Simple wrapper for a SAT solver (Spear)
    '''
    
    def get_command_line_args(self, runargs, config):
        '''
        Returns the command line call string to execute the target algorithm (here: Spear).
        Args:
            runargs: a map of several optional arguments for the execution of the target algorithm.
                    {
                      "instance": <instance>,
                      "specifics" : <extra data associated with the instance>,
                      "cutoff" : <runtime cutoff>,
                      "runlength" : <runlength cutoff>,
                      "seed" : <seed>
                    }
            config: a mapping from parameter name to parameter value
        Returns:
            A command call list to execute the target algorithm.
        '''
        binary_path = "~/src/trellis/bin/trellis"
        binary_path = os.path.expanduser(binary_path)
        cmd = "%s -f %s" %(binary_path, runargs["instance"])
        #, runargs["seed"])       
        for name, value in config.items():
            value=value.replace("'","")
            cmd += " -%s %s" %(name,  value)
        return cmd
    
    def process_results(self, filepointer, out_args):
        '''
        Parse a results file to extract the run's status (SUCCESS/CRASHED/etc) and other optional results.
    
        Args:
            filepointer: a pointer to the file containing the solver execution standard out.
            out_args : a map with {"exit_code" : exit code of target algorithm} 
        Returns:
            A map containing the standard AClib run results. The current standard result map as of AClib 2.06 is:
            {
                "status" : <"SUCCESS"/"SAT"/"UNSAT"/"TIMEOUT"/"CRASHED"/"ABORT">,
                "runtime" : <runtime of target algrithm>,
                "quality" : <a domain specific measure of the quality of the solution [optional]>,
                "misc" : <a (comma-less) string that will be associated with the run [optional]>
            }
            ATTENTION: The return values will overwrite the measured results of the runsolver (if runsolver was used). 
        '''
        data = filepointer.read()

        #print data
        import json
        lines = ''
        iterator = iter(data.split('\n'))
        print iterator
        try:
            while True:
                value=iterator.next()
                if value == '' or value.startswith('c'):
                    continue
                else:
                    break
        except StopIteration, e:
            pass

        try:
            resultMap=json.loads(value)
            resultMap['status'] = 'SUCCESS'
            resultMap['quality'] = resultMap['width']
            #print resultMap
        except ValueError, e:
            pass
        return resultMap

if __name__ == "__main__":
    wrapper = SatWrapper()
    wrapper.main()    
