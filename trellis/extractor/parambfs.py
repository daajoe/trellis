# noinspection PyRedundantParentheses
import copy, os
from itertools import permutations

import random
import networkx as nx
# from networkx.drawing.nx_agraph import graphviz_layout, write_dot
# import matplotlib.pyplot as plt
# #import matplotlib

from trellis.extractor.extractor import Extractor
from trellis.td import TreeDecomposition


class ParamExtractor(Extractor):
    @staticmethod
    def bfs(decomp, max_bag_size=None, budget=50, rand=False, c1=1.0, c2=0.5, beta=5, gamma=10, delta=2):
        # get the bags from the tree decomposition
        """

        :param budget: the number of vertices in the local decomp
        :param max_bag_size: the bagsize from where we want to start bfs
        :type decomp: decomposition
        """
        rest_decomp = copy.deepcopy(decomp)
        bag_lengths = dict(zip(decomp.bags.keys(), map(len, decomp.bags.values())))
        bags = decomp.bags
        # root of the BFS is the bag with max elements
        root_id = decomp.get_first_node(max_bag_size)
        root = bag_lengths.keys()[root_id]
        bfs_queue = [root]
        bfs_depth = dict()
        bfs_common_nodes = {}
        parent = {}
        # initialization for BFS
        for i in decomp.tree.nodes():
            bfs_depth[i] = -1
            parent[i] = -1
        bfs_depth[root] = 0
        parent[root] = root
        internal_nodes = []
        bfs_common_nodes[root] = decomp.bags[root]
        sub_vertices = set(decomp.bags[root])
        # root is the internal node should not be deleted from the local tree
        internal_nodes.append(root)
        # maybe change this part Not sure how to avoid this.
        while bfs_queue:
            # show_graph(decomp.tree, 1)
            # print "BFS:", bfs_queue
            if rand:
                random.shuffle(bfs_queue)
            v2 = bfs_queue.pop(0)
            # print v2,bfs_queue
            # print v2,decomp.tree[v2]
            # if any of the neighbours have a bag of size > current bag do not continue on this bag
            # changing the checking to the intersection of two bags i.e. check how many vertices are common.
            for w in decomp.tree[v2]:
                flag = 0
                if bfs_depth[w] == -1:
                    parent[w] = v2
                    bfs_common_nodes[w] = bags[w].intersection(bags[v2])
                    bfs_depth[w] = bfs_depth[v2] + 1
                    if c1 * len(bags[w]) - c2 * len(bfs_common_nodes[w]) <= 1:
                        if w not in bfs_queue and w not in internal_nodes:
                            bfs_queue.append(w)
                        if w not in internal_nodes:
                            internal_nodes.append(w)
                            sub_vertices |= decomp.bags[w]
                        continue
                    if bfs_depth[w] <= beta:
                        if w not in bfs_queue and w not in internal_nodes:
                            bfs_queue.append(w)
                        if w not in internal_nodes:
                            internal_nodes.append(w)
                            sub_vertices |= decomp.bags[w]
                        continue
                    sub_tree = ParamExtractor.subtree(decomp, w, v2)
                    if len(sub_tree) <= gamma:
                        for w1 in sub_tree:
                            if w1 not in bfs_queue and w1 not in internal_nodes:
                                bfs_queue.append(w1)
                                bfs_depth[w1] = bfs_depth[w] + 1
                                parent[w1] = w
                            if w1 not in internal_nodes:
                                internal_nodes.append(w1)
                                sub_vertices |= decomp.bags[w1]
                        continue
                    else:
                        flag = 1
                if flag == 1:
                    new_node = max(rest_decomp.tree.nodes()) + 1
                    rest_decomp.tree.add_node(new_node)
                    rest_decomp.tree.add_edge(new_node, w)
                    rest_decomp.tree.add_edge(new_node, parent[w])
                    rest_decomp.tree.remove_edge(w, parent[w])
                    rest_decomp.bags[new_node] = set(bfs_common_nodes[w])
                    if w in internal_nodes:
                        internal_nodes.remove(w)
                    if new_node not in internal_nodes:
                        internal_nodes.append(new_node)
                if len(sub_vertices) >= budget + delta * max_bag_size:
                    break
        print len(internal_nodes), len(sub_vertices)
        # rest_decomp.show(layout=1)
        return internal_nodes, sub_vertices, rest_decomp

    @staticmethod
    def subtree(decomp, w, v):
        neigh = decomp.tree.neighbors(w)
        neigh.remove(v)
        dfs_visited = [w]
        while neigh:
            try:
                n = neigh.pop()
                dfs_visited.append(n)
                for i in decomp.tree.neighbors(n):
                    if i in dfs_visited:
                        continue
                    neigh.append(i)
            except StopIteration:
                break
        return dfs_visited

    @staticmethod
    def extract_graph(internal_nodes, decomp, g):
        """
        generates graph for the local tree decomposition
        ASSUMPTION: vertices have not been relabelled
        :return:
        :param g: input graph type: Networkx Graph
        :param internal_nodes: nodes of tree decomposition which are picked by BFS  type: list
        :param decomp: Tree decomposition type: Networkx Graph
        :return: sub_graph: graph generated by the local tree decomposition by adding clique for all leaf nodes/bags type: networkx graph
        :return: rest_decomp: Sub Tree Decomposition after removing the local tree decomposition type: networkx Graph
        :return: connecting_leave: The leaves where local tree decomposition connects with the rest_decomp type:list
    -    """
        y = decomp.tree.subgraph(internal_nodes)
        # show_graph(y,layout=1)
        sub_nodes = set()
        for n in y.nodes():
            sub_nodes |= set(decomp.bags[n])
        connecting_nodes = {}
        sub_graph = g.subgraph(sub_nodes)
        for leaf, degree in y.degree().iteritems():
            if degree != 1:
                continue
            if decomp.tree.degree(leaf) > y.degree(leaf):
                internal_nodes.remove(leaf)
                connecting_nodes[leaf] = decomp.bags[leaf]
            for i, j in permutations(decomp.bags[leaf], r=2):
                sub_graph.add_edge(i, j)
        rest_decomp = TreeDecomposition(tree=decomp.tree.subgraph(set(decomp.tree.nodes()) - set(internal_nodes)))
        #TODO:
        #,
        # temp_path=self.temp_path,
        # delete_temp=self.delete_temp, plot_if_td_invalid=self.plot_if_td_invalid
        for i in internal_nodes:
            del decomp.bags[i]
        rest_decomp.bags = decomp.bags
        return sub_graph, rest_decomp, connecting_nodes

    @staticmethod
    def extract_decomposition(decomp, g, max_bag_size=None, budget=50,
                              extractor_args={'extractor_c1': 1.0, 'extractor_c2': 0.5, 'extractor_beta': 3,
                                              'extractor_gamma': 5, 'extractor_random': False, 'extractor_delta': 2}):
        internal_nodes, _, rest_decomp = ParamExtractor.bfs(decomp, max_bag_size=max_bag_size, budget=budget,
                                                            c1=extractor_args['extractor_c1'],
                                                            c2=extractor_args['extractor_c2'],
                                                            beta=extractor_args['extractor_beta'],
                                                            gamma=extractor_args['extractor_gamma'],
                                                            rand=extractor_args['extractor_random'],
                                                            delta=extractor_args['extractor_delta'])
        sub_graph, rest_decomp, connecting_leaves = ParamExtractor.extract_graph(internal_nodes,
                                                                                 copy.deepcopy(rest_decomp), g)
        # exit(0)
        return rest_decomp, sub_graph, connecting_leaves

    @staticmethod
    def connect_decomp(rest_decomp, sub_decomp, connecting_nodes, graph, td_name, always_validate=True):
        if rest_decomp.tree.number_of_nodes() == 0:
            return TreeDecomposition(tree=sub_decomp.tree, bags=sub_decomp.bags, graph=graph, td_name=td_name)
        new_decomp = nx.union(rest_decomp.tree, sub_decomp.tree)
        for node, bag in connecting_nodes.iteritems():
            connect = True
            for key, value in sub_decomp.bags.iteritems():
                rest_decomp.bags[key] = value
                if bag.issubset(value) and connect:
                    new_decomp.add_edge(node, key)
                    connect = False
        td = TreeDecomposition(tree=new_decomp, bags=rest_decomp.bags, graph=graph, td_name=td_name)
        if always_validate:
            td.validate2()
        return td

#
# def show_graph(graph, layout, nolabel=0, write=0, file_name=None, dnd=0, labels=None):
#     """ show graph
#     layout 1:graphviz,
#     2:circular,
#     3:spring,
#     4:spectral,
#     5: random,
#     6: shell
#     """
#     if dnd == 0:
#         m = graph.copy()
#         pos = graphviz_layout(m)
#         if layout == 1:
#             pos = graphviz_layout(m)
#         elif layout == 2:
#             pos = nx.circular_layout(m)
#         elif layout == 3:
#             pos = nx.spring_layout(m)
#         elif layout == 4:
#             pos = nx.spectral_layout(m)
#         elif layout == 5:
#             pos = nx.random_layout(m)
#         elif layout == 6:
#             pos = nx.shell_layout(m)
#         if not nolabel:
#             nx.draw_networkx_edge_labels(m, pos)
#         nx.draw_networkx_nodes(m, pos)
#         if labels:
#             labels = {k: '%s:%s'%(k,str(sorted(list(v)))) for k,v in labels.iteritems()}
#             nx.draw_networkx_labels(m, pos, labels)
#         else:
#             nx.draw_networkx_labels(m, pos)
#         if write != 0:
#             write_dot(m, file_name + ".dot")
#             os.system("dot -Tps " + file_name + ".dot -o " + file_name + '.ps')
#         else:
#             # plt.ion()
#             # nx.draw(m, pos)
#             # plt.plot(m,pos)
#             nx.draw(m, pos)
#             # plt.show(block=False)
#             plt.show()
