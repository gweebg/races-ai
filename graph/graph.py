import math
from queue import Queue
from typing import Dict, List, Tuple, Any
from collections import deque

# Biblioteca de tratamento de grafos necessária para desenhar graficamente o grafo
import networkx as nx
# Biblioteca de tratamento de grafos necessária para desenhar graficamente o grafo
import matplotlib.pyplot as plt


class Graph:
    def __init__(self, directed=False) -> None:
        self.graph = {}
        self.is_directed = directed
        self.heur = {}

    def add_edge(self, val1, val2, weight) -> None:
        if val1 not in self.graph:
            self.graph[val1] = {}

        self.graph[val1][val2] = weight

        if val2 not in self.graph:
            self.graph[val2] = {}

        if not self.is_directed:
            self.graph[val2][val1] = weight

    def add_val(self, val) -> None:
        if val not in self.graph:
            self.graph[val] = {}

    def has_val(self, node) -> bool:
        return node in self.graph

    def get_weight(self, val1, val2) -> int | None:
        if val1 in self.graph:
            return self.graph[val1][val2]
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
            cost += self.graph[path[i - 1]][path[i]]

        return cost

    def add_heuristic(self, val, heur):
        self.heur[val] = heur

    def dfs(self, start, end, path=None, visited=None) -> tuple[list, int] | None:
        if visited is None:
            visited = set()
        if path is None:
            path = []

        path.append(start)
        visited.add(start)

        if start == end:
            custo = self.path_cost(path)
            return path, custo
        for (adjacente, pesos) in self.graph[start].items():
            if adjacente not in visited:
                resultado = self.dfs(adjacente, end, path, visited)
                if resultado is not None:
                    return resultado
        path.pop()
        return None

    def bfs(self, start, end, comp_function) -> tuple[list, int] | None:
        visited = set()
        fila = Queue()

        fila.put(start)
        visited.add(start)

        parent = dict()
        parent[start] = None

        path_found = False
        while not fila.empty() and path_found is False:
            nodo_atual = fila.get()
            if comp_function(nodo_atual, end):
                path_found = True
            else:
                for (adjacente, peso) in self.graph[nodo_atual].items():
                    if adjacente not in visited:
                        fila.put(adjacente)
                        parent[adjacente] = nodo_atual
                        visited.add(adjacente)

        path = []
        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
            # funçao calcula custo caminho
            custo = self.path_cost(path)
            return path, custo

        return None

    def get_neighbours(self, nodo) -> list:
        lista = []
        for (adjacente, peso) in self.graph[nodo].items():
            lista.append((adjacente, peso))
        return lista

    def greedy(self, start, end) -> tuple[list, int] | None:
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

            if n == end:
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

    def a_star(self, start, end) -> tuple[list, int] | None:
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

            if n == end:
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
                    g[m] = g[n] + weight[0]

            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None

    def draw(self):
        lista_v = self.graph.keys()
        lista_a = []
        g = nx.Graph()

        # Converter para o formato usado pela biblioteca networkx
        for nodo in lista_v:
            g.add_node(nodo)
            for (adjacente, peso) in self.graph[nodo].items():
                lista = (nodo, adjacente)
                # lista_a.append(lista)
                g.add_edge(nodo, adjacente, weight=peso)

        # desenhar o grafo
        pos = nx.spring_layout(g)
        nx.draw_networkx(g, pos, with_labels=True, font_weight='bold')
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)

        plt.draw()
        plt.show()
