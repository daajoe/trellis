#!/usr/bin/env python
from optparse import OptionParser
import select
from sys import stderr, stdin, stdout

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

for line in inp.readlines():
    line=line.split()
    if line==[]:
        continue
    if line[0]!='p':
        stdout.write('edge({},{}).\n'.format(line[0],line[1]))

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
