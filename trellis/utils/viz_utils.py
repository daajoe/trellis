#!/usr/bin/env python
# coding=utf-8
import os
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout, write_dot
#import matplotlib.pyplot as plt
#import matplotlib

def show_graph(graph, layout, nolabel=0, write=0, file_name=None, dnd=0, labels=None):
    """ show graph
    layout 1:graphviz,
    2:circular,
    3:spring,
    4:spectral,
    5: random,
    6: shell
    """
    return
    matplotlib.use('TkAgg')
    if dnd == 0:
        m = graph.copy()
        pos = graphviz_layout(m)
        if layout == 1:
            pos = graphviz_layout(m)
        elif layout == 2:
            pos = nx.circular_layout(m)
        elif layout == 3:
            pos = nx.spring_layout(m)
        elif layout == 4:
            pos = nx.spectral_layout(m)
        elif layout == 5:
            pos = nx.random_layout(m)
        elif layout == 6:
            pos = nx.shell_layout(m)
        if not nolabel:
            nx.draw_networkx_edge_labels(m, pos)
        nx.draw_networkx_nodes(m, pos)
        if labels:
            labels = {k: '%s:%s'%(k,str(sorted(list(v)))) for k,v in labels.iteritems()}
            nx.draw_networkx_labels(m, pos, labels)
        else:
            nx.draw_networkx_labels(m, pos)
        if write != 0:
            write_dot(m, file_name + ".dot")
            os.system("dot -Tps " + file_name + ".dot -o " + file_name + '.ps')
        else:
            # plt.ion()
            # nx.draw(m, pos)
            # plt.plot(m,pos)
            nx.draw(m, pos)
            # plt.show(block=False)
            plt.show()
