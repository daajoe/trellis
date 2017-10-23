#!/usr/bin/env false
# coding=utf-8
from __future__ import print_function
import gzip
from bz2 import BZ2File
from itertools import count, izip
import backports.lzma as xz

import mimetypes
import networkx as nx


def complete_graph(vertices):
    g1 = nx.complete_graph(len(vertices))
    g1 = nx.relabel_nodes(g1, mapping=dict(izip(g1.nodes(), vertices)), copy=True)
    return g1


class Graph(nx.Graph):
    def __init__(self, data=None, val=None, **attr):
        super(Graph, self).__init__()
        self.val = val

    @staticmethod
    def from_file(filename):
        """
        :param filename: name of the file to read from
        :type filename: string
        :rtype: Graph
        :return: a list of edges and number of vertices
        """
        return Graph._from_file(filename)

    @staticmethod
    def dimacs_header(filename):
        """
        :param filename: name of the file to read from
        :type filename: string
        :return: a list of edges and number of vertices
        """
        return Graph._from_file(filename, header_only=True)

    @staticmethod
    def _from_file(filename, header_only=False):
        """
        :param filename: name of the file to read from
        :type filename: string
        :param header_only: read header only
        :rtype: Graph
        :return: imported graph
        """
        num_edges = None
        num_verts = None
        is_dimacs = False
        stream = None
        graph = Graph()
        try:
            mtype = mimetypes.guess_type(filename)[1]
            if mtype is None:
                stream = open(filename, 'r')
            elif mtype == 'bzip2':
                stream = BZ2File(filename, 'r')
            elif mtype == 'gz':
                stream = gzip.open(filename, 'r')
            elif mtype == 'xz':
                stream = xz.open(filename, 'r')
            else:
                raise IOError('Unknown input type "%s" for file "%s"' % (mtype, filename))
            for line in stream:
                line = line.split()
                if line == [] or line[0] in ('x', 'n'):
                    continue
                if line[0] == 'p':
                    is_dimacs = line[1] == 'edge'
                    num_verts = int(line[2])
                    num_edges = int(line[3])
                    if header_only:
                        return num_verts, num_edges
                elif line[0] != 'c':
                    if is_dimacs:
                        graph.add_edge(int(line[1]), int(line[2]))
                    else:
                        graph.add_edge(int(line[0]), int(line[1]))
        finally:
            if stream:
                stream.close()

        if graph.number_of_edges() < num_edges:
            print("edges missing: read=%s announced=%s" % (graph.number_of_edges(), num_edges))
        if graph.number_of_nodes() < num_verts:
            print("vertices missing: read=%s announced=%s" % (graph.number_of_edges(), num_edges))
        return graph

    def write_dimacs(self, stream, copy=True):
        return self.write_graph(stream, copy, dimacs=True)

    def write_gr(self, stream, copy=True):
        return self.write_graph(stream, copy, dimacs=False)

    def write_graph(self, stream, copy=True, dimacs=False):
        """
        :param stream: stream where to output the graph
        :type stream: cString
        :param copy: return a copy of the original graph
        :type copy: bool
        :param dimacs: write dimacs header (or gr header)
        :type dimacs: bool
        :rtype Graph, dict
        :return: written graph, remapping of vertices from old graph
        """
        mapping = {org_id: id for id, org_id in izip(count(start=1), self.nodes_iter())}
        graph = nx.relabel_nodes(self, mapping, copy=copy)
        gr_string = 'edge' if dimacs else 'tw'
        s = 'p ' if dimacs else ''
        stream.write('p %s %s %s\n' % (gr_string, graph.number_of_nodes(), graph.number_of_edges()))
        for u, v in graph.edges_iter():
            stream.write('%s%s %s\n' % (s, u, v))
        stream.flush()
        return graph, mapping
