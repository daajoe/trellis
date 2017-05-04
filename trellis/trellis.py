#!/usr/bin/env python
# coding=utf-8

import argparse
import cStringIO
import json
import logging
import logging.config
import signal
import tempfile
from tempfile import NamedTemporaryFile

from localdecomp import *
from utils.graph_utils import make_graph, write_graph
from utils.htd_utils import convert_pacestring2nxdecomp, generate_trivial_decomp, max_bag_size, write_decomp
from utils.signals import AbortException, handler, nothing
from utils.viz_utils import show_graph


def setup_logging(config_file='%s/logging.conf' % (os.path.dirname(__file__))):
    logging.config.fileConfig(config_file)


setup_logging(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logging.conf'))

def validate_td(graph, td, temp_path='/tmp', type='org'):
    with NamedTemporaryFile(mode='w', dir=temp_path, delete=True) as graph_stream:
        write_graph(graph_stream, graph, copy=True)
        with NamedTemporaryFile(mode='w', dir=temp_path, delete=True) as ostream:
            written_decomp = write_decomp(ostream, td)
            cmd = 'td-validate %s %s' % (graph_stream.name, ostream.name)
            validator = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True, close_fds=True)
            output, err = validator.communicate()
            if not err.startswith('valid'):
                print '--- STDOUT ---'
                print type, output
                print '--- STDERR ---'
                print err
                # show_graph(td[0], 1, labels=td[1])
                print 'written_decomp(tree)=', written_decomp[0].edges()
                print 'written_decomp(bags)=', written_decomp[1]
                show_graph(written_decomp[0], 1, labels=written_decomp[1])
                exit(1)


def bag_verts(bags):
    ret = set()
    for i in bags.itervalues():
        for j in i:
            ret.add(j)
    return sorted(list(ret))


def decomp_subgraph_pace(graph, temp_path, solver_path, solver_args='', timeout=30):
    # type: (nx.graph, basestring, basestring, integer) -> tuple
    dirname = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
    sys.path.append(dirname)
    from pace_solvers.pace_solver_call import compute_decomp
    with NamedTemporaryFile(mode='w', dir=temp_path, delete=False) as tmp_file:
        vertex_mapping, graph = write_graph(tmp_file, graph, copy=True)
        ret = compute_decomp(tmp_file.name, solver_path=solver_path, solver_args=solver_args, timeout=timeout)
        # convert string into nx.td
        td_max_bag_size, td = convert_pacestring2nxdecomp(ret)
        if not td_max_bag_size:
            return None, td, vertex_mapping, graph
    sys.stderr.write('Subgraph Result(max_bag_size): %s\n' % td_max_bag_size)
    return td_max_bag_size, td, vertex_mapping, graph


def decomp_subgraph_sat(temp_path, sub_graph, graph_max_bag_size, time_out, encoder, solver, solver_args):
    # write graph
    with NamedTemporaryFile(mode='w', dir=temp_path, delete=False) as tmp2:
        vertex_mapping = write_graph(tmp2, sub_graph, copy=False)

        logging.info('Max-Len=%s', graph_max_bag_size)

        assignment, width, elapsed_time = find_width_ubound(tmp2.name, time_out, encoder, solver, solver_args,
                                                            ubound=graph_max_bag_size - 1, tmp=temp_path)
        subgraph_bag_size = width + 1
        nodes = read_sol_nh(assignment, sub_graph.number_of_nodes())
        sub_decomp = compute_decomp(sub_graph.copy(), order=nodes)
    return width, sub_decomp, vertex_mapping


# noinspection SpellCheckingInspection
def local_improve(fname, temp_path, path, time_out, encoder, solver_path, solver_args, budget, subsolver_budget,
                  usehtd=True, presolver_timeout=5):
    initial_htd_max_bag_size = 0
    new_decomp = (None, {})
    rounds = improved_rounds = last_improved_round = 0
    org_graph = make_graph(fname)
    subgraph_max_numb_verts = subgraph_max_numb_edges = -1
    res = None

    try:
        if budget == -1:
            budget = min(org_graph.number_of_nodes() * 3 / 4, 70)
        graph = org_graph

        decomp, graph_max_bag_size = generate_pre_decomp(graph, path, temp_path, timeout=presolver_timeout,
                                                         htd=usehtd)
        res = graph_max_bag_size
        if graph_max_bag_size == 0:
            signal.signal(signal.SIGTERM, nothing)
            signal.signal(signal.SIGINT, nothing)

            return initial_htd_max_bag_size, initial_htd_max_bag_size, \
                   (rounds, improved_rounds, last_improved_round), \
                   (org_graph.number_of_nodes(), org_graph.number_of_edges(), subgraph_max_numb_verts,
                    subgraph_max_numb_edges), \
                   False
        validate_td(graph=graph.copy(), td=decomp, temp_path=temp_path, type='initial')
        initial_htd_max_bag_size = graph_max_bag_size
        sat_budget = subsolver_budget

        while sat_budget > 0:
            rounds += 1
            cdecomp = copy.deepcopy(decomp)
            sys.stderr.write('old_maxbag(before everything) = %s; \n' % max_bag_size(decomp))

            rest_decomp, sub_graph, connecting_nodes = extract_decomp_edge(decomp, graph, graph_max_bag_size,
                                                                           budget)
            sys.stderr.write(
                'cmax_bag_size = %s (%s); sub_graph(#verts) = %s ; graph(#verts) = %s; budget = %s ; subsolver_runs = %s\n' % (
                    graph_max_bag_size, max_bag_size(decomp), sub_graph.number_of_nodes(), graph.number_of_nodes(),
                    budget,
                    sat_budget))

            subgraph_max_numb_verts = max(sub_graph.number_of_nodes(), subgraph_max_numb_verts)
            subgraph_max_numb_edges = max(sub_graph.number_of_edges(), subgraph_max_numb_edges)

            sub_decomp_max_bag_size, sub_decomp, vertex_mapping, sub_graph = decomp_subgraph_pace(sub_graph,
                                                                                                  temp_path,
                                                                                                  solver_path=solver_path,
                                                                                                  solver_args=solver_args,
                                                                                                  timeout=time_out)
            if sub_decomp_max_bag_size is None or sub_decomp_max_bag_size > graph_max_bag_size:
                sat_budget -= 1
                decomp = cdecomp
                new_decomp = cdecomp
                sys.stderr.write(
                    'Worse sub-decomp or no sub-decomp from subsolver. Proceeding without applying it.\n')
                continue
            validate_td(graph=sub_graph.copy(), td=sub_decomp, temp_path=temp_path, type='sub')

            sub_decomp = convert_to_small_decomposition(sub_decomp)
            sub_decomp = relabel_sub_decomp(sub_decomp, max(rest_decomp[0].nodes() + [0]) + 1, vertex_mapping)
            new_decomp = connect_decomp(rest_decomp, sub_decomp, connecting_nodes)

            # REQUIRED BECAUSE WE MAY HAVE DUPLICATE BAGS
            validate_td(graph=org_graph.copy(), td=new_decomp, temp_path=temp_path, type='before small')
            new_decomp = convert_to_small_decomposition(new_decomp)
            validate_td(graph=org_graph.copy(), td=new_decomp, temp_path=temp_path, type='updated')

            if not (max_bag_size(new_decomp) < graph_max_bag_size):
                sat_budget -= 1
            else:
                sat_budget = subsolver_budget
                last_improved_round = rounds
                improved_rounds += 1
                res = max_bag_size(new_decomp)
            decomp = new_decomp
            graph_max_bag_size = max_bag_size(new_decomp)
        sys.stderr.write('INITIAL VALUE WAS max_bags=%s\n' % initial_htd_max_bag_size)
        sys.stderr.write('RESULT max_bags=%s\n' % max_bag_size(new_decomp))
        sys.stderr.write('RESULT width=%s\n' % (max_bag_size(new_decomp) - 1))

        signal.signal(signal.SIGTERM, nothing)
        signal.signal(signal.SIGINT, nothing)
        return (initial_htd_max_bag_size, res, (rounds, improved_rounds, last_improved_round),
                (org_graph.number_of_nodes(), org_graph.number_of_edges(),
                 subgraph_max_numb_verts, subgraph_max_numb_edges), True)
    except AbortException, e:
        signal.signal(signal.SIGTERM, nothing)
        signal.signal(signal.SIGINT, nothing)

        return (initial_htd_max_bag_size, res, (rounds, improved_rounds, last_improved_round),
                (org_graph.number_of_nodes(), org_graph.number_of_edges(),
                 subgraph_max_numb_verts, subgraph_max_numb_edges), False)


def generate_pre_decomp(graph, path, temp_path, htd=True, timeout=5):
    with NamedTemporaryFile(mode='w', dir=temp_path, delete=False) as tmp_file:
        write_graph(tmp_file, graph, copy=False)
        htd_stream = cStringIO.StringIO()
        if htd:
            compute_ordering_htd(tmp_file.name, htd_stream, path, timeout=timeout, iterations=100, seed=0)
        else:
            compute_ordering_flow_cutter(tmp_file.name, htd_stream, path, timeout=timeout)
        # compute_ordering_htd_mock(tmp_file.name, htd_stream, path, iterations=100, seed=0)
        htd_stream.seek(0)
        max_bag_size, decomp = convert_pacestring2nxdecomp(htd_stream.getvalue())
    return decomp, max_bag_size


def generate_decomp_trivial(graph, path=None, tmp_file=None):
    decomp, graph_max_bag_size = generate_trivial_decomp(graph)
    return decomp, graph_max_bag_size


def parse_args():
    parser = argparse.ArgumentParser(description='%s -f instance')
    parser.add_argument('-f', '--file', dest='instance', action='store', type=lambda x: os.path.realpath(x),
                        help='instance', required=True)
    parser.add_argument('-e', '--encoder', dest='encoder', action='store', type=lambda x: find_executable(x),
                        help='encoder_binary', default='tw2cnf')
    parser.add_argument('-s', '--solver', dest='solver', action='store', type=lambda x: find_executable(x),
                        help='solver_binary', default=find_executable('tcs-meiji'))
    parser.add_argument('-a', '--solver-args', dest='solver_args', action='store', type=str,
                        help='solver_args', default='')
    parser.add_argument('-w', '--solver-wall-clock-limit', dest='timelimit', action='store', type=int,
                        help='time-limit',
                        default=900)
    parser.add_argument('--runid', dest='runid', action='store', type=int, help='id of the current repeation',
                        default=1)
    parser.add_argument('-b', '--bfs-budget', dest='budget', action='store', type=int, help='bfs budget',
                        default=10)
    parser.add_argument('-r', '--subsolver-budget', dest='subsolver_budget', action='store', type=int,
                        help='subsolver retry budget',
                        default=10)
    parser.add_argument('-t', '--tmp', dest='tmp', action='store', type=str, help='unused',
                        default=tempfile.gettempdir())
    parser.add_argument('-p', '--pre-solver', dest='presolver', action='store', type=str, help='select presolver',
                        default='htd', choices=['htd', 'flow_cutter'])
    parser.add_argument('-x', '--presolver-wall-clock-limit', dest='presolver_timeout', action='store', type=int,
                        help='presolver runtime limit', default=15)
    args = parser.parse_args()
    if args.presolver == 'htd':
        args.usehtd = True
    else:
        args.usehtd = False
    if not os.path.isfile(args.instance):
        sys.stderr.write('File "%s" does not exist.\n' % args.instance)
        exit(16)
    return args


def main():
    args = parse_args()
    fname = args.instance
    solver = args.solver
    temp_path = args.tmp
    timeout = args.timelimit
    encoder = args.encoder
    path = os.path.dirname(fname)
    solver_args = args.solver_args
    runid = args.runid
    subsolver_budget = args.subsolver_budget
    budget = args.budget
    usehtd = args.usehtd
    presolver_timeout = args.presolver_timeout

    p = Popen(['sha256sum', args.instance], stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    rc = p.returncode
    sha = output.split()[0]

    wallstart = time.time()
    err = ''

    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)
    sys.stderr.write('solver = %s\n' % solver)

    wallstart = time.time()
    h_ubound_max_bag_size, li_ubound_max_bag_size, (rounds_overall, rounds_improved, last_improved_round), \
    (graph_max_numb_verts, graph_max_numb_edges, subgraph_max_numb_verts, subgraph_max_numb_edges), solved \
        = local_improve(fname, temp_path, path, timeout, encoder, solver, solver_args, budget, subsolver_budget,
                        presolver_timeout=presolver_timeout, usehtd=usehtd)
    wall = time.time() - wallstart

    try:
        solver_name = os.path.basename(solver)
    except AttributeError, e:
        solver_name = 'unknown_iternal'
    res = {'instance': fname, 'width': li_ubound_max_bag_size - 1, 'ubound': h_ubound_max_bag_size - 1, 'wall': wall,
           'solver': solver_name, 'hash': sha, 'args': vars(args), 'solved': int(solved), 'err': err, 'run': runid,
           # 'system_info': get_system_info(),
           'rounds': rounds_overall, 'rounds_improved': rounds_improved, 'last_improved_in_round': last_improved_round,
           'subgraph_max_verts': subgraph_max_numb_verts, 'subgraph_max_edges': subgraph_max_numb_edges,
           'inputgraph_max_verts': graph_max_numb_verts, 'inputgraph_max_edges': graph_max_numb_edges,
           'bfs_budget': budget, 'subsolver_budget': subsolver_budget}
    sys.stdout.write(json.dumps(res, sort_keys=True))
    sys.stdout.write('\n')
    sys.stdout.flush()
    exit(0)


if __name__ == "__main__":
    main()
