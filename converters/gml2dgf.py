#!/usr/bin/env python
from optparse import OptionParser
import select
from sys import stderr, stdin, stdout
import networkx as nx
import re

fromfile=True
if select.select([stdin,],[],[],0.0)[0]:
    inp=stdin
    fromfile=False
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


#strict implementation of gml "edge \n [ -> edge ["
string = re.sub(r'\s+\[', ' [', ''.join(inp.readlines()))

G = nx.parse_gml(string)
stream = stdout

stream.write('p edge %s %s\n' %(G.number_of_nodes(), G.number_of_edges()))
for u,v in G.edges():
    stream.write('%s %s\n' %(u,v))


if fromfile:
    inp.close()

try:
    stdout.close()
except:
    pass

try:
    stderr.close()
except:
    pass
