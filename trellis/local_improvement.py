import copy
import logging
import logging.config
import signal

from trellis import decomposer
from trellis.extractor.edges import EdgeExtractor
from trellis.graph import Graph
from trellis.td import TreeDecomposition
from trellis.utils.signals import nothing, AbortException


class LocalImprovement(object):
    # TODO: move solver to solver class
    def __init__(self, filename, global_solver, local_solver):
        """
        :param filename:
        :type filename: string
        :param global_solver:
        :type global_solver: Decomposer
        :param local_solver:
        :type local_solver: Decomposer
        """

        self.rounds = 0
        self.rounds_improved = 0
        self.rounds_last_improved = 0
        self.localgraph_max_num_verts = -1
        self.localgraph_max_numb_edges = -1
        self.local_solver = local_solver
        self.global_solver = global_solver
        self.filename = filename
        self.globalsolver_mbsize = 0
        self.res = None
        self.inputgraph_number_of_verts = None
        self.inputgraph_number_of_edges = None
        self.solved = False
        self.lb = self.lt = self.gt = None

    def statistics(self):
        return dict(instance=self.filename, width=self.res - 1, li_mbsize=self.res,
                    ubound_mbsize=self.globalsolver_mbsize, ubound=self.globalsolver_mbsize - 1,
                    globalsolver=self.global_solver.name, localsolver=self.local_solver.name,
                    solved=int(self.solved), rounds=self.rounds, rounds_improved=self.rounds_improved,
                    last_improved_in_round=self.rounds_last_improved, subgraph_max_verts=self.localgraph_max_num_verts,
                    subgraph_max_edges=self.localgraph_max_numb_edges,
                    inputgraph_max_verts=self.inputgraph_number_of_verts,
                    inputgraph_max_edges=self.inputgraph_number_of_edges, lb=self.lb, lt=self.lt, gt=self.gt)

    # noinspection SpellCheckingInspection
    def decompose(self, lt, lb, extractor=None, ni=10, gt=60):
        """
        :param lt: local timeout
        :type lt: integer
        :param lb: local budget
        :type lb: integer
        :param extractor:
        :type extractor: Extractor
        :param ni: number of no-improvement rounds
        :type ni: integer
        :param gt: global timeout
        :type gt: integer
        :rtype: TreeDecomposition
        :returns a tree decomposition of the initialized file using the defined global solver and local solver
        """
        self.lb = lb
        self.lt = lt
        self.gt = gt
        if not extractor:
            extractor = EdgeExtractor
        inputgraph = Graph.from_file(self.filename)
        self.inputgraph_number_of_verts = inputgraph.number_of_nodes()
        self.inputgraph_number_of_verts = inputgraph.number_of_nodes()
        new_decomp = TreeDecomposition(graph=inputgraph, td_name='org')

        # MAIN: computation
        try:
            # TODO:
            if lb == -1:
                lb = min(inputgraph.number_of_nodes() * 3 / 4, 70)
            global_td, _, _ = self.global_solver.decompose(graph=inputgraph, timeout=gt)
            self.res = global_td.max_bag_size()
            graph_max_bag_size = global_td.max_bag_size()
            if global_td.max_bag_size() == 0:
                signal.signal(signal.SIGTERM, nothing)
                signal.signal(signal.SIGINT, nothing)
                return new_decomp

            global_td.validate(graph=inputgraph, type='initial')
            self.globalsolver_mbsize = global_td.max_bag_size()
            lb_remaining = ni

            while lb_remaining > 0:
                self.rounds += 1
                cdecomp = copy.deepcopy(global_td)
                logging.warn('old_maxbag(before everything) = %s' % global_td.max_bag_size())
                rest_decomp, localgraph, connecting_nodes = extractor.extract_decomposition(global_td, inputgraph,
                                                                                            graph_max_bag_size,
                                                                                            lb)
                logging.warn(
                    'cmax_bag_size = %s (%s); localgraph(#verts) = %s ; inputgraph(#verts) = %s; budget = %s ; '
                    'subsolver_runs = %s' % (
                        graph_max_bag_size, global_td.max_bag_size(), localgraph.number_of_nodes(),
                        inputgraph.number_of_nodes(),
                        lb, lb_remaining))

                self.localgraph_max_num_verts = max(localgraph.number_of_nodes(), self.localgraph_max_num_verts)
                self.localgraph_max_numb_edges = max(localgraph.number_of_edges(), self.localgraph_max_numb_edges)

                local_td, vertex_mapping, localgraph = self.local_solver.decompose(graph=localgraph, timeout=lt,
                                                                                   name='sub')
                # applies to heuristic subsolver
                if local_td.max_bag_size() is None or local_td.max_bag_size() > graph_max_bag_size:
                    lb_remaining -= 1
                    global_td = cdecomp
                    new_decomp = cdecomp
                    logging.warn('Worse sub-decomp or no sub-decomp from subsolver. Proceeding without applying it.')
                    continue
                local_td.simplify()
                local_td = local_td.relabeled_decomposition(max(rest_decomp.tree.nodes() + [0]) + 1, vertex_mapping)

                new_decomp = extractor.connect_decomp(rest_decomp, local_td, connecting_nodes,
                                                      graph=inputgraph.copy(), td_name='connected')
                new_decomp.simplify()
                if not (new_decomp.max_bag_size() < graph_max_bag_size):
                    lb_remaining -= 1
                else:
                    lb_remaining = lb
                    self.rounds_last_improved = self.rounds
                    self.rounds_improved += 1
                    self.res = new_decomp.max_bag_size()
                global_td = new_decomp
                graph_max_bag_size = new_decomp.max_bag_size()
            logging.warn('INITIAL VALUE WAS max_bags=%s' % self.globalsolver_mbsize)
            logging.warn('RESULT max_bags=%s' % new_decomp.max_bag_size())
            logging.warn('RESULT width=%s' % (new_decomp.max_bag_size() - 1))

            signal.signal(signal.SIGTERM, nothing)
            signal.signal(signal.SIGINT, nothing)
            self.solved = True
            return new_decomp
        except AbortException as e:
            signal.signal(signal.SIGTERM, nothing)
            signal.signal(signal.SIGINT, nothing)
            return new_decomp
