#!/usr/bin/env false
# coding=utf-8

import networkx as nx


def reduction(g):
    while True:
        if g.number_of_nodes() >= 1 and min(g.degree().values()) == 0:
            node = min(g.degree(), key=g.degree().get)
            g.remove_node(node)
            continue
        elif g.number_of_nodes() >= 1 and min(g.degree().values()) == 1:
            node = min(g.degree(), key=g.degree().get)
            g.remove_node(node)
            continue
        elif g.number_of_nodes() >= 1 and min(g.degree().values()) == 2:
            node = min(g.degree(), key=g.degree().get)
            neigh = list(g.neighbors(node))
            g.add_edge(neigh[0], neigh[1])
            g.remove_node(node)
            continue
        break
    return nx.convert_node_labels_to_integers(g, first_label=1)


def reduce_graph(g):
    g1 = list(nx.biconnected_component_subgraphs(g))
    for f1 in g1:
        # TODO: might not work due to hiding in the function reduction
        reduction(f1)
    return g1
