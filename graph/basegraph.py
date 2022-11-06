from graph.node import Node

from math import inf

import networkx as nx
import matplotlib.pyplot as plt


class BaseGraph:

    def __init__(self, is_directed: bool = False):
        self.nodes: list[Node] = []  # List of every existing node.
        self.graph = {}  # Dictionary containing the graph itself.
        self.is_directed = is_directed

    def add_edge(self, node_a: Node, node_b: Node, cost: int) -> None:

        if node_a not in self.nodes:
            self.nodes.append(node_a)
            self.graph[node_a.name] = []
        else:
            node_a = self.get_node_by_name(node_a.name)

        if node_b not in self.nodes:
            self.nodes.append(node_b)
            self.graph[node_b.name] = []
        else:
            node_b = self.get_node_by_name(node_b.name)

        self.graph[node_a.name].append((node_b.name, cost))

        if not self.is_directed:
            self.graph[node_b.name].append((node_a.name, cost))

    def get_edge_cost(self, node_a: Node, node_b: Node) -> float:

        final_cost: float = inf
        node_a_edges: list[(str, int)] = self.graph[node_a.name]

        for (node_name, cost) in node_a_edges:
            if Node(node_name) == node_b:
                final_cost = cost

        return final_cost

    def get_path_cost(self, path: list[Node]) -> float:

        cost: float = 0
        idx: int = 0

        while idx + 1 < len(path):
            cost = cost + self.get_edge_cost(path[idx], path[idx + 1])
            idx += 1

        return cost

    def get_path_cost_by_name(self, path: list[str]) -> float:

        cost: float = 0
        idx: int = 0

        while idx + 1 < len(path):
            cost = cost + self.get_edge_cost(Node(path[idx]), Node(path[idx + 1]))
            idx += 1

        return cost

    def get_node_by_name(self, node_name: str) -> Node | None:
        searching_node: Node = Node(node_name)

        for node in self.nodes:
            if node == searching_node:
                return node

        return None

    def edges_as_text(self):
        edges: str = ""
        graph_keys = self.graph.keys()

        for node_a in graph_keys:
            for (node_b, node_cost) in self.graph[node_a]:
                edges = edges + f"{node_a}---{node_cost}---{node_b}\n"

        return edges

    def get_node_neighbours(self, node: Node):
        neighbours: list = []

        for (adjacent, weight) in self.graph[node.name]:
            neighbours.append((adjacent, weight))

        return neighbours

    def draw(self):
        graph_as_nx = nx.Graph()

        for node in self.nodes:
            graph_as_nx.add_node(node.name)

            for (adjacent, cost) in self.graph[node.name]:
                graph_as_nx.add_edge(node.name, adjacent, weight=cost)

        pos = nx.spring_layout(graph_as_nx)
        nx.draw_networkx(graph_as_nx, pos, with_labels=True)

        labels = nx.get_edge_attributes(graph_as_nx, 'weight')
        nx.draw_networkx_edge_labels(graph_as_nx, pos, edge_labels=labels)

        plt.draw()
        plt.show()

    def __str__(self):
        graph: str = ""
        for edge in self.graph:
            graph = graph + f"Node {str(edge)}: {str(self.graph[edge])}\n"
        return graph
