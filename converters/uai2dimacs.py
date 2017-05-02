#!/usr/bin/env python
from optparse import OptionParser
import select,os
from sys import stderr, stdin, stdout
import networkx as nx
import numpy as np
from itertools import permutations


def uai_to_dimacs(fstream,ostream):
    """

    :param fname: file name type: string
    :return: a list of edges and number of vertices
    """
    num_edges = None
    num_verts = None
    dimacs = False
    network= False
    network_type = None
    line=fstream.readline()
    if line[0]=='M':
        network_type='M'
    elif line[0] == 'B':
        network_type='B'
    else:
        raise TypeError("wrong type")
    line=fstream.readline()
    line=line.split()
    num_verts=int(line[0])
    line=fstream.readline()
    line=fstream.readline()
    line=line.split()
    num_edges=int(line[0])
    ne=0
    adjacency_list=np.zeros((num_verts,num_verts),dtype=int)
    if network_type=='M':
        for linecount in xrange(num_edges):
            line = fstream.readline()
            line = line.split()
            func=int(line.pop(0))
            if func>1:
                for i,j in permutations(line,r=2):
                    if not adjacency_list[int(i)][int(j)]:
                        adjacency_list[int(i)][int(j)]=1
                        adjacency_list[int(j)][int(i)]=1
                        ne+=1
    if network_type=='B':
        for linecount in xrange(num_edges):
            line = fstream.readline()
            line = line.split()
            func=int(line.pop(0))
            if func>1:
                k=int(line.pop())
                for i in line:
                    if not adjacency_list[int(i)][k]:
                        adjacency_list[int(i)][k]=1
                        adjacency_list[k][int(i)]=1
                        ne+=1
                for i,j in permutations(line,r=2):
                    if not adjacency_list[int(i)][int(j)]:
                        adjacency_list[int(i)][int(j)]=1
                        adjacency_list[int(j)][int(i)]=1
                        ne+=1
    ostream.write("p edge %i %i\n" % (num_verts, ne))
    for i in xrange(num_verts):
        for j in xrange(i+1,num_verts):
            if adjacency_list[i][j]:
                ostream.write("e %i %i\n"%(i+1,j+1))


fromfile=True
if select.select([stdin,],[],[],0.0)[0]:
    inp=stdin
    fromfile=False
    out=stdout
else:
    parser = OptionParser()
    parser.add_option('-f', '--file', dest='filename',
                  help='Input file', metavar='FILE')
    (options, args) = parser.parse_args()
    if not options.filename:
        stderr.write('Missing filename')
        parser.print_help(stderr)
        stderr.write('\n')
        exit(1)
    inp = open(options.filename, 'r')
    fromfile=True
    fname, ext = os.path.splitext(os.path.basename(options.filename))
    out = open(fname+'.edge','w')
uai_to_dimacs(inp,out)



if fromfile:
    inp.close()
    out.close()

try:
    stdout.close()
except:
    pass

try:
    stderr.close()
except:
    pass
