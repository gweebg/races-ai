from graph.basegraph import BaseGraph
from graph.node import Node

from queue import Queue


class SearchGraph(BaseGraph):

    def __init__(self, is_directed: bool = False):
        super().__init__(is_directed)

    def dfs_search(self, start: str, end: str, path=None, visited=None):

        if visited is None:
            visited = set()

        if path is None:
            path = []

        path.append(start)
        visited.add(start)

        if start == end:
            cost = self.get_path_cost_by_name(path)
            return path, cost

        for (adjacent, weight) in self.graph[start]:
            if adjacent not in visited:
                result = self.dfs_search(adjacent, end, path, visited)
                if result is not None:
                    return result

        path.pop()
        return None

    def bfs_search(self, start, end):

        visited = set()
        queue = Queue()

        queue.put(start)
        visited.add(start)

        parent = dict()
        parent[start] = None

        path_found: bool = False
        while not queue.empty() and not path_found:
            current_node = queue.get()

            if current_node == end:
                path_found = True
            else:
                for (adjacent, weight) in self.graph[current_node]:
                    if adjacent not in visited:
                        queue.put(adjacent)
                        parent[adjacent] = current_node
                        visited.add(adjacent)

        path = []
        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]

            path.reverse()
            cost = self.get_path_cost_by_name(path)
            return path, cost

        return None
