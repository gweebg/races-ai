import matplotlib.pyplot as plt
import networkx as nx

from typing import Optional, Any
from queue import Queue


class Graph:
    def __init__(self, directed=False) -> None:
        self.graph = {}
        self.is_directed = directed
        self.heur = {}

    def add_edge(self, val1, val2, weight) -> None:
        if val1 not in self.graph:
            self.graph[val1] = {}

        self.graph[val1][val2] = weight, True

        if val2 not in self.graph:
            self.graph[val2] = {}

        if not self.is_directed:
            self.graph[val2][val1] = weight, True
        elif val1 not in self.graph[val2]:
            self.graph[val2][val1] = weight, False

    def remove_edge(self, val1, val2) -> None:
        del self.graph[val1][val2]
        if not self.is_directed:
            del self.graph[val2][val1]

    def add_val(self, val) -> None:
        if val not in self.graph:
            self.graph[val] = {}

    def has_val(self, node) -> bool:
        return node in self.graph

    def get_weight(self, val1, val2) -> int | None:
        if val1 in self.graph:
            return self.graph[val1][val2][0]
        else:
            return None

    def __str__(self) -> str:
        ret = ""

        for (node, edges) in self.graph.items():
            ret += "'{}':\n".format(node)
            for (node2, weight) in edges.items():
                ret += "    ('{}', {});\n".format(node2, weight)
            ret += '\n'

        return ret

    def path_cost(self, path):
        cost = 0
        assert len(path) >= 2
        for i in range(1, len(path)):
            cost += self.graph[path[i - 1]][path[i]][0]

        return cost

    def get_neighbours(self, nodo) -> list:
        lista = []
        for (adjacente, (peso, b)) in self.graph[nodo].items():
            lista.append((adjacente, peso))
        return lista

    def get_all_associated(self, val) -> tuple[list[Any], list[Any]]:
        lista_ir = []
        lista_vir = []
        for (adjacente, (peso, b)) in self.graph[val].items():
            lista_ir.append((adjacente, peso))
            if val in self.graph[adjacente]:
                (peso2, valid) = self.graph[adjacente][val]
                if valid:
                    lista_vir.append((adjacente, peso2))
        return lista_ir, lista_vir

    def add_heuristic(self, val, heur):
        self.heur[val] = heur

    def has_heuristic(self, val):
        return val in self.heur

    # Search Functions #

    def dfs_search(self, start_node, end_node_list, path=None, visited=None) -> Optional[tuple[list, int]]:

        if visited is None:
            visited = set()

        if path is None:
            path = list()

        path.append(start_node)
        visited.add(start_node)

        if start_node in end_node_list:
            cost = self.path_cost(path)
            return path, cost

        for (adjacent_node, weight) in self.graph[start_node].items():

            if adjacent_node not in visited:
                result = self.dfs_search(adjacent_node, end_node_list, path, visited)

                if result:
                    return result

        path.pop()
        return None

    def bfs_search(self, start_node, end_node_list) -> Optional[tuple[list, int]]:

        visited = set()
        queue = Queue()

        queue.put(start_node)
        visited.add(start_node)

        parent = dict()
        parent[start_node] = None

        path_found = False
        end_node_found = None
        while not queue.empty() and not path_found:

            current_node = queue.get()

            if current_node in end_node_list:
                end_node_found = current_node
                path_found = True

            else:
                for (adjacent_node, weight) in self.graph[current_node].items():

                    if adjacent_node not in visited:

                        queue.put(adjacent_node)
                        parent[adjacent_node] = current_node
                        visited.add(adjacent_node)

        path = []
        cost = 0
        if path_found:

            path.append(end_node_found)

            while parent[end_node_found]:

                path.append(parent[end_node_found])
                end_node_found = parent[end_node_found]

            path.reverse()
            cost = self.path_cost(path)

        return path, cost

    def greedy_search(self, start, end_list) -> tuple[list, int] | None:
        open_list = {start}
        closed_list = set([])

        parents = {start: start}

        while len(open_list) > 0:
            n = None

            for v in open_list:
                if n is None or self.heur[v] < self.heur[n]:
                    n = v

            if n is None:
                print('Path does not exist!')
                return None

            if n in end_list:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return reconst_path, self.path_cost(reconst_path)

            for (m, weight) in self.get_neighbours(n):
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n

            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None

    def a_star_search(self, start, end_list) -> tuple[list, int] | None:
        open_list = {start}
        closed_list = set([])

        parents = {start: start}

        g = {start: 0}

        while len(open_list) > 0:
            n = None

            for v in open_list:
                if n is None or self.heur[v] + g[v] < self.heur[n] + g[n]:
                    n = v

            if n is None:
                print('Path does not exist!')
                return None

            if n in end_list:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return reconst_path, self.path_cost(reconst_path)

            for (m, weight) in self.get_neighbours(n):
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight

            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None

    def draw(self):

        nodes = self.graph.keys()
        graph = nx.Graph()

        for node in nodes:
            graph.add_node(node)

            for (adjacent_node, weight) in self.graph[node].items():
                graph.add_edge(node, adjacent_node, weight=weight)

        layout = nx.spring_layout(graph)
        nx.draw_networkx(graph, layout, with_labels=True, font_weight='bold')

        labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, layout, edge_labels=labels)

        plt.draw()
        plt.show()
