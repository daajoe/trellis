import logging
from itertools import count, imap
from itertools import izip
from operator import itemgetter
from tempfile import NamedTemporaryFile

import networkx as nx
import subprocess

import os
from networkx.drawing.nx_agraph import graphviz_layout, write_dot


class TreeDecomposition(object):
    lib_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../libs/'))
    folder_name = 'tdvalidate'
    bin_name = 'tdvalidate'

    path = os.path.join(lib_path, folder_name, bin_name)

    # TODO: add debugging type
    # add graph as parameter
    def __init__(self, tree=None, bags=None, td_name=None, graph=None, always_validate=True, temp_path='/tmp'):
        self.always_validate = always_validate
        self.graph = graph
        self.name = td_name
        self.temp_path = temp_path
        self.tree = nx.Graph() if not tree else tree
        self.bags = {} if not bags else bags
        self.delete_temp = True if not __debug__ else False

    def __len__(self):
        return len(self.bags)

    def validate(self, graph, type='org'):
        graph = graph.copy()
        with NamedTemporaryFile(mode='w', dir=self.temp_path, delete=self.delete_temp) as graph_stream:
            graph.write_gr(graph_stream)
            with NamedTemporaryFile(mode='w', dir=self.temp_path, delete=self.delete_temp) as ostream:
                written_decomp = self.write(ostream)
                cmd = '%s %s %s' % (self.path, graph_stream.name, ostream.name)
                validator = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                             close_fds=True)
                output, err = validator.communicate()
                rc = int(validator.returncode)
                if rc != 0:
                    for line in err.split('\n'):
                        if len(line) == 0:
                            continue
                        logging.critical(line)
                    logging.warning('Return code was "%s"' % rc)
                    if rc == 127:
                        logging.warning(
                            'Consult README and check whether td-validate has been build correctly with cmake.')

                    exit(rc)

                if not err.startswith('valid'):
                    logging.error('--- STDOUT ---')
                    logging.error(type, output)
                    logging.error('--- STDERR ---')
                    logging.error(err)
                    written_decomp.show(layout=1)
                    exit(1)

    def validate2(self, name=None):
        if not name:
            name = self.name
        graph = self.graph.copy()
        with NamedTemporaryFile(mode='w', dir=self.temp_path, delete=self.delete_temp) as graph_stream:
            graph.write_gr(graph_stream)
            with NamedTemporaryFile(mode='w', dir=self.temp_path, delete=self.delete_temp) as ostream:
                written_decomp = self.write(ostream)
                cmd = '%s %s %s' % (self.path, graph_stream.name, ostream.name)
                validator = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                             close_fds=True)
                output, err = validator.communicate()
                rc = int(validator.returncode)
                if rc != 0:
                    for line in err.split('\n'):
                        if len(line) == 0:
                            continue
                        logging.critical(line)
                    logging.warning('Return code was "%s"' % rc)
                    if rc == 127:
                        logging.warning(
                            'Consult README and check whether td-validate has been build correctly with cmake.')
                        logging.warning('CMD = %s' %cmd)

                    exit(rc)

                if not err.startswith('valid'):
                    logging.error('--- STDOUT ---')
                    logging.error('name=%s, output=%s' % (name, output))
                    logging.error('--- STDERR ---')
                    logging.error(err)
                    # TODO:
                    # written_decomp.show(layout=1)
                    exit(1)
                return True

    def write(self, ostream):
        tree_mapping = {org_id: id for id, org_id in izip(count(start=1), self.tree.nodes_iter())}
        tree = nx.relabel_nodes(self.tree, tree_mapping, copy=True)
        max_bag_size = reduce(max, map(len, self.bags.itervalues() or [0]))
        num_vertices = reduce(lambda x, y: max(x, max(y or [0])), self.bags.itervalues(), 0)
        ostream.write('s td %s %s %s\n' % (len(self.bags), max_bag_size, num_vertices))

        relabeled_bags = {tree_mapping[k]: v for k, v in self.bags.iteritems()}
        relabeled_bags = sorted(relabeled_bags.items(), key=itemgetter(0))
        for bag_id, bag in relabeled_bags:
            ostream.write('b %s %s\n' % (bag_id, ' '.join(imap(str, bag))))
        for u, v in tree.edges_iter():
            ostream.write('%s %s\n' % (u, v))
        ostream.flush()
        return TreeDecomposition(tree=tree, bags=dict(relabeled_bags))

    def max_bag_size(self):
        ret = 0
        for b in self.bags.itervalues():
            ret = max(ret, len(b))
        return ret

    def get_first_node(self, max_bag_size):
        bagids2lengths = dict(zip(self.bags.keys(), map(len, self.bags.values())))
        lengths = bagids2lengths.values()
        if not max_bag_size:
            max_bag_size = max(lengths)
        root_id = lengths.index(max_bag_size)
        return bagids2lengths.keys()[root_id]

    def relabeled_decomposition(self, offset, vertex_mapping, inplace=False):
        if inplace:
            raise NotImplementedError("Not implemented yet.")
        offset += 1
        tree_mapping = {org_id: id for id, org_id in izip(count(start=offset), self.tree.nodes_iter())}
        new_bags = {}
        for i in xrange(offset, offset + len(self.tree.nodes())):
            new_bags[i] = self.bags[self.tree.nodes()[i - offset]]
        ret_tree = nx.relabel_nodes(self.tree, tree_mapping, copy=False)
        # relabeled_decomposition the contents of the bags according to mapping
        inv_mapping = dict(imap(reversed, vertex_mapping.items()))
        for key, bag in new_bags.iteritems():
            new_bags[key] = set(map(lambda x: inv_mapping[x], bag))
        # TODO: refactor
        return TreeDecomposition(tree=ret_tree, bags=new_bags)

    def show(self, layout, nolabel=0):
        """ show graph
        layout 1:graphviz,
        2:circular,
        3:spring,
        4:spectral,
        5: random,
        6: shell
        """
        if not __debug__:
            logging.error('written_decomp(tree)=%s', self.tree.edges())
            logging.error('written_decomp(bags)=%s', self.bags)

            return
        else:
            import matplotlib.pyplot as plt
            import matplotlib

            matplotlib.use('TkAgg')

            m = self.tree.copy()
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
            if self.bags:
                bags = {k: '%s:%s' % (k, str(sorted(list(v)))) for k, v in self.bags.iteritems()}
                nx.draw_networkx_labels(m, pos, bags)
            else:
                nx.draw_networkx_labels(m, pos)
            nx.draw(m, pos)
            plt.show()

    def simplify(self):
        node = iter(self.tree.nodes())
        while True:
            try:
                i = next(node)
                neigh_list = set(self.tree[i])
                for neigh in self.tree[i]:
                    if self.bags[i].issubset(self.bags[neigh]):
                        for neigh1 in neigh_list - set([neigh]):
                            self.tree.add_edge(neigh, neigh1)
                        self.tree.remove_node(i)
                        del self.bags[i]
                        break
            except StopIteration:
                break
        if self.always_validate:
            self.validate2()


class TrivialTreeDecomposition(TreeDecomposition):
    def __init__(self):
        super(TrivialTreeDecomposition, self).__init__()

    def from_graph(self, graph):
        self.bags = {1: graph.nodes()}
        self.tree.add_node(1)
