#!/usr/bin/env python
# coding=utf-8

import networkx as nx
from subprocess import Popen, PIPE, call
import sys
# from viz_utils import *
from itertools import imap, izip, count, chain
from operator import itemgetter


# noinspection PyUnusedLocal
def compute_ordering_htd_mock(file_name, ostream, path, iterations=100, seed=0):
    with open('%s/../../LI-encodings/test/Brinkmann-htd.decomp' % path) as f:
        ostream.write('\n'.join(f.readlines()))


def compute_ordering_htd(file_name, ostream, path, timeout=5, iterations=100, seed=0):
    #min-fill          Minimum fill ordering algorithm (default)
    #min-degree        Minimum degree ordering algorithm
    #max-cardinality   Maximum cardinality search ordering algorithm
    #challenge
    #min-degree
    cmd = 'timeout %s %s --iterations %i --seed %i --opt width --input gr --strategy challenge < %s' % (
        timeout, 'htd_main', iterations, seed, file_name)
    sys.stderr.write(cmd + '\n')
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True, cwd=path)
    output, err = p.communicate()
    sys.stderr.write(err)
    ostream.write(output)
    rc = p.returncode
    # sys.stderr.write(ostream.getvalue())
    if rc != 0:
        sys.stderr.write('Runtime error. htd returned "%s"' % rc)
        raise RuntimeError('Runtime error. htd returned "%s"' % rc)


def compute_ordering_flow_cutter(file_name, ostream, path, timeout=20):
    cmd = 'timeout %s %s < %s' % (timeout, 'flow_cutter', file_name)
    sys.stderr.write(cmd + '\n')
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True, cwd=path)
    output, err = p.communicate()
    sys.stderr.write(err)
    ostream.write(output)
    rc = p.returncode
    if rc not in (0, 124):
        sys.stderr.write('Runtime error. htd returned "%s"' % rc)
        raise RuntimeError('Runtime error. htd returned "%s"' % rc)


def generate_decomp_nh(stream):
    s = stream.readline().split()
    decomp = nx.Graph()
    nodes = list()
    for _ in range(int(s[2])):
        s1 = stream.readline().split()
        s1.pop(0)
        s1.pop(0)
        s1 = [int(i) for i in s1]
        decomp.add_node(frozenset(sorted(s1)))
        nodes.append(frozenset(sorted(s1)))
    for _ in range(int(s[2]) - 1):
        s1 = stream.readline().split()
        decomp.add_edge(nodes[int(s1[0]) - 1], nodes[int(s1[1]) - 1])
    return decomp


def generate_trivial_decomp(graph):
    tree = nx.Graph()
    bags = {1: graph.nodes()}
    tree.add_node(1)
    return (tree, bags), graph.number_of_nodes()

def max_bag_size(decomp):
    ret = 0
    for b in decomp[1].itervalues():
        ret = max(ret, len(b))
    return ret


def convert_pacestring2nxdecomp(lines):
    if lines == '':
        sys.stderr.write('No input string from subsolver.\n')
        return None, (nx.Graph(), {})
    bags = {}
    graph = nx.Graph()
    num_bags = td_max_bag_size = num_vertices = 0
    for line in lines.split('\n'):
        line = line.split()
        # noinspection PySimplifyBooleanCheck
        if line == []:
            continue
        if line[0] == 'c':
            sys.stderr.write('%s\n' % ' '.join(line))
            continue
        elif line[0] == 's' and line[1] == 'td':
            num_bags, td_max_bag_size, num_vertices = map(int, line[2:])
            # sys.stderr.write('%s\n' % str(line))
        elif line[0] == 'b':
            bag_name = int(line[1])
            bags[bag_name] = set(map(int, line[2:]))
            graph.add_node(bag_name)
        else:
            u, v = map(int, line)
            graph.add_edge(u, v)
    # decomps of single bags require special treatment
    if len(bags) == 1:
        # noinspection PyUnresolvedReferences
        graph.add_node(bags.iterkeys().next())
    if len(bags) != num_bags:
        sys.stderr.write('WARNING: Number of bags differ. Was %s expected %s.\n' % (len(bags), num_bags))
    if len(set(chain.from_iterable(bags.itervalues()))) != num_vertices:
        sys.stderr.write(
            'WARNING: Number of vertices differ. Was %s expected %s.\n' % (graph.number_of_nodes(), num_vertices))
    if max_bag_size((None, bags)) != td_max_bag_size:
        sys.stderr.write(
            'WARNING: Number of vertices differ. Was %s expected %s.\n' % (max_bag_size((None, bags)), td_max_bag_size))
    return td_max_bag_size, (graph, bags)


# DOES RELABELLING
def write_decomp(ostream, td):
    tree = td[0]
    tree_mapping = {org_id: id for id, org_id in izip(count(start=1), tree.nodes_iter())}

    tree = nx.relabel_nodes(tree, tree_mapping, copy=True)
    bags = td[1]
    max_bag_size = reduce(max, map(len, bags.itervalues() or [0]))

    # RELABEL BAGS:
    num_vertices = reduce(lambda x, y: max(x, max(y or [0])), bags.itervalues(), 0)
    ostream.write('s td %s %s %s\n' % (len(bags), max_bag_size, num_vertices))

    relabeled_bags = {tree_mapping[k]: v for k, v in bags.iteritems()}
    relabeled_bags = sorted(relabeled_bags.items(), key=itemgetter(0))
    for id, bag in relabeled_bags:
        ostream.write('b %s %s\n' % (id, ' '.join(imap(str, bag))))
    for u, v in tree.edges_iter():
        ostream.write('%s %s\n' % (u, v))
    ostream.flush()
    return (tree, dict(relabeled_bags))
