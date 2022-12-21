from typing import Any
from enum import Enum
from graph.graph import Graph


class TransactionType(Enum):
    ADD_EDGE = 0
    REM_EDGE = 1
    ADD_VAL = 2
    ADD_HEUR = 3


class ImmGraphTransaction:
    t_data: list[tuple[TransactionType, tuple[Any, ...]]]

    def __init__(self):
        self.t_data = []

    def add_edge(self, val1, val2, weight) -> 'ImmGraphTransaction':
        self.t_data.append((TransactionType.ADD_EDGE, (val1, val2, weight)))
        return self

    def remove_edge(self, val1, val2) -> 'ImmGraphTransaction':
        self.t_data.append((TransactionType.REM_EDGE, (val1, val2)))
        return self

    def add_val(self, val) -> 'ImmGraphTransaction':
        self.t_data.append((TransactionType.ADD_VAL, tuple(val)))
        return self

    def add_heur(self, val, heur) -> 'ImmGraphTransaction':
        self.t_data.append((TransactionType.ADD_HEUR, (val, heur)))
        return self


class ImmGraph(Graph):

    def apply_transaction(self, transaction: ImmGraphTransaction) -> 'ImmGraph':
        if len(transaction.t_data) == 0:
            return self

        igraph = ImmGraph(self.is_directed)
        igraph.graph = self.graph
        igraph.heur = self.heur
        graph_copy = False
        heur_copy = False

        for trans_type, args in transaction.t_data:
            match trans_type:
                case TransactionType.ADD_EDGE:
                    if not graph_copy:
                        igraph.graph = igraph.graph.copy()
                        graph_copy = True
                    igraph.__priv_add_edge(*args)

                case TransactionType.REM_EDGE:
                    if not graph_copy:
                        igraph.graph = igraph.graph.copy()
                        graph_copy = True
                    igraph.__priv_remove_edge(*args)

                case TransactionType.ADD_VAL:
                    if not graph_copy:
                        igraph.graph = igraph.graph.copy()
                        graph_copy = True
                    igraph.__priv_add_val(*args)

                case TransactionType.ADD_HEUR:
                    if not heur_copy:
                        igraph.heur = igraph.heur.copy()
                        heur_copy = True
                    igraph.__priv_add_heuristic(*args)

        return igraph

    def add_edge(self, val1, val2, weight) -> 'ImmGraph':
        igraph = ImmGraph(self.is_directed)
        igraph.graph = self.graph.copy()
        igraph.heur = self.heur
        igraph.__priv_add_edge(val1, val2, weight)
        return igraph

    def __priv_add_edge(self, val1, val2, weight) -> None:
        if val1 not in self.graph:
            self.graph[val1] = {}
        else:
            self.graph[val1] = self.graph[val1].copy()

        self.graph[val1][val2] = weight

        if val2 not in self.graph:
            self.graph[val2] = {}

        if not self.is_directed:
            self.graph[val2] = self.graph[val2].copy()
            self.graph[val2][val1] = weight

    def add_val(self, val) -> 'ImmGraph':
        igraph = ImmGraph(self.is_directed)
        igraph.graph = self.graph.copy()
        igraph.heur = self.heur
        igraph.__priv_add_val(val)
        return igraph

    def __priv_add_val(self, val) -> None:
        if val not in self.graph:
            self.graph[val] = {}

    def add_heuristic(self, val, heur) -> 'ImmGraph':
        igraph = ImmGraph(self.is_directed)
        igraph.graph = self.graph
        igraph.heur = self.heur.copy()
        igraph.__priv_add_heuristic(val, heur)
        return igraph

    def __priv_add_heuristic(self, val, heur) -> None:
        self.heur[val] = heur

    def remove_edge(self, val1, val2) -> 'ImmGraph':
        igraph = ImmGraph(self.is_directed)
        igraph.graph = self.graph.copy()
        igraph.heur = self.heur
        igraph.__priv_remove_edge(val1, val2)
        return igraph

    def __priv_remove_edge(self, val1, val2) -> None:
        self.graph[val1] = self.graph[val1].copy()
        del self.graph[val1][val2]
        if not self.is_directed:
            self.graph[val2] = self.graph[val2].copy()
            del self.graph[val2][val1]

    @staticmethod
    def wrap_graph(graph: Graph) -> 'ImmGraph':
        igraph = ImmGraph(graph.is_directed)
        igraph.graph = graph.graph
        igraph.heur = graph.heur
        return igraph
