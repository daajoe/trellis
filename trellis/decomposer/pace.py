import logging
import os
import subprocess
import sys
from itertools import chain
from tempfile import NamedTemporaryFile

from trellis.td import TreeDecomposition
from trellis.decomposer.decomposer import Decomposer


class PACEDecomposer(Decomposer):
    lib_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../libs/'))
    args = ['']

    def __init__(self, temp_path, args='', always_validate=True):
        self.always_validate = always_validate
        self.args = args
        self.temp_path = temp_path
        # from distutils import spawn

    def decompose(self, graph, timeout=30, name=None):
        # type: (Graph, integer) -> tuple
        # TODO: change to cStringIO.StringIO()?
        with NamedTemporaryFile(mode='w', dir=self.temp_path, delete=False) as tmp_file:
            relabeled_graph, vertex_mapping = graph.write_gr(tmp_file)
            ret = self.call_solver(tmp_file.name, timeout=timeout)
            # convert string into nx.td
            td = PACEDecomposer.pacestr2nxdecomp(ret, graph=relabeled_graph, name=name)
            if td.max_bag_size() is None:
                return td, vertex_mapping, relabeled_graph
        logging.info('Subgraph Result(max_bag_size): %s' % td.max_bag_size())
        if self.always_validate:
            td.validate2()
        return td, vertex_mapping, relabeled_graph

    @staticmethod
    def pacestr2nxdecomp(lines, graph, name):
        """

        :param lines:
        :param graph:
        :param name:
        :rtype: TreeDecomposition
        :return:
        """
        td = TreeDecomposition(graph=graph, td_name=name)
        if lines == '':
            sys.stderr.write('No input string from solver.')
            # TODO:
            # raise RuntimeWarning('No input string from subsolver.\n')
            return td
        num_bags = td_max_bag_size = num_vertices = 0
        for line in lines.split('\n'):
            line = line.split()
            # noinspection PySimplifyBooleanCheck
            if line == []:
                continue
            if line[0] == 'c':
                logging.warning('-' * 20 + 'INFO from solver' + '-' * 20)
                logging.warning('%s' % ' '.join(line))
                logging.warning('-' * 80)
                continue
            elif line[0] == 's' and line[1] == 'td':
                num_bags, td_max_bag_size, num_vertices = map(int, line[2:])
                # sys.stderr.write('%s\n' % str(line))
            elif line[0] == 'b':
                bag_name = int(line[1])
                td.bags[bag_name] = set(map(int, line[2:]))
                td.tree.add_node(bag_name)
            else:
                u, v = map(int, line)
                td.tree.add_edge(u, v)
        # decomps of single bags require special treatment
        if len(td) == 1:
            # noinspection PyUnresolvedReferences
            td.tree.add_node(td.bags.iterkeys().next())
        if len(td) != num_bags:
            sys.stderr.write('WARNING: Number of bags differ. Was %s expected %s.\n' % (len(td), num_bags))
        if len(set(chain.from_iterable(td.bags.itervalues()))) != num_vertices:
            sys.stderr.write(
                'WARNING: Number of vertices differ. Was %s expected %s.\n' % (td.tree.number_of_nodes(), num_vertices))
        if td.max_bag_size() != td_max_bag_size:
            sys.stderr.write(
                'WARNING: Number of vertices differ. Was %s expected %s.\n' % (
                    td.max_bag_size(), td_max_bag_size))
        return td

    def call(self, cmd):
        logging.warning('CMD= "%s"' % cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        rc = p.returncode
        if rc != 0 or err != '':
            for line in err.split('\n'):
                logging.warning(line)
        return output

    # TODO: fix
    def call_solver(self, instance_path, timeout=30, iterations=None):
        path = os.path.join(self.lib_path, self.folder_name, self.bin_name)
        cmd = 'timeout %i %s %s < %s' % (
            timeout, path, self.args.replace('"', '').replace("&quot;", ""), instance_path)
        return self.call(cmd)
