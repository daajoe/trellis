#!/usr/bin/env python
# coding=utf-8
import gzip
from bz2 import BZ2File
from itertools import count, izip

import mimetypes
import networkx as nx


def read_hyper_graph(fname, graph, header_only=False):
    """

    :param fname: file name type: string
    :return: a list of edges and number of vertices
    """
    num_edges = None
    num_verts = None
    dimacs = False
    fstream = None

    try:
        mtype = mimetypes.guess_type(fname)[1]
        if mtype is None:
            fstream = open(fname, 'r')
        elif mtype == 'bzip2':
            fstream = BZ2File(fname, 'r')
        elif mtype == 'gz':
            fstream = gzip.open(fname, 'r')
        else:
            raise IOError('Unknown input type "%s" for file "%s"' % (mtype, fname))
        for line in fstream:
            line = line.split()
            if line == [] or line[0] in ('x', 'n'):
                continue
            if line[0] == 'p':
                dimacs = line[1] == 'edge'
                num_verts = int(line[2])
                num_edges = int(line[3])
                if header_only:
                    return num_verts, num_edges
            elif line[0] != 'c':
                if dimacs:
                    graph.add_edge(int(line[1]), int(line[2]))
                else:
                    graph.add_edge(int(line[0]), int(line[1]))
    finally:
        if fstream:
            fstream.close()

    if graph.number_of_edges() < num_edges:
        print "edges missing: read=%s announced=%s" % (graph.number_of_edges(), num_edges)
    if graph.number_of_nodes() < num_verts:
        print "vertices missing: read=%s announced=%s" % (graph.number_of_edges(), num_edges)
    return graph


def make_graph(file_name):
    """

    :param file_name: graph file without extension type : string
    :return: networkx graph
    """
    G = nx.Graph()
    return read_hyper_graph(file_name, G)


def write_graph(stream, org_graph, copy=True, dimacs=False):
    mapping = {org_id: id for id, org_id in izip(count(start=1), org_graph.nodes_iter())}
    graph = nx.relabel_nodes(org_graph, mapping, copy=copy)
    gr_string = 'edge' if dimacs else 'tw'
    s = 'p ' if dimacs else ''
    stream.write('p %s %s %s\n' % (gr_string, graph.number_of_nodes(), graph.number_of_edges()))
    for u, v in graph.edges_iter():
        stream.write('%s%s %s\n' % (s, u, v))
    stream.flush()
    return mapping, graph


def add_node_bag(g, bags, bag):
    g.add_node()
    key = g.number_of_nodes()
    bags[key] = frozenset(bag)
    return key


def get_bag(decomp, size=-1):
    """

    :returns a bag of size from decomp

    :param decomp: Tree decomposition type: networkx Graph
    :param size: size of the bag to be found default: Max size type: int
    :return: bag of size
    """
    if size == -1:
        size = max([len(i1) for i1 in decomp.nodes()])
    for i in decomp.nodes():
        if len(i) == size:
            return i
