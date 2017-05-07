#!/usr/bin/env false

from abc import ABCMeta, abstractmethod


class Decomposer(object):
    __metaclass__ = ABCMeta
    name = None

    @abstractmethod
    def decompose(self, graph, timeout):
        pass
