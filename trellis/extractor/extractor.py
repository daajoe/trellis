from abc import ABCMeta, abstractmethod


class Extractor(object):
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def bfs(decomp, max_bag_size=None, budget=50):
        pass

    @staticmethod
    @abstractmethod
    def extract_graph(internal_nodes, decomp, g):
        pass


    @staticmethod
    @abstractmethod
    def extract_decomposition(decomp, g, max_bag_size=None, budget=50):
        pass

    @staticmethod
    @abstractmethod
    def connect_decomp(rest_decomp, sub_decomp, connecting_nodes, graph, td_name, always_validate=True):
        pass
