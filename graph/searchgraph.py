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

    def astar_search(self, start: str, end: str):

        open_list: set = {start}
        closed_list: set = set([])

        from_start_dist: dict = {start: 0}
        parents: dict = {start: start}

        current_node = None
        while len(open_list) > 0:

            calculate_heuristic = {}
            flag = 0

            for node_name in open_list:
                if current_node is None:
                    current_node = node_name
                else:
                    flag = 1
                    calculate_heuristic[node_name] = from_start_dist[node_name] + self.get_node_heuristic(node_name)

            if flag == 1:
                min_estimate = self.calculate_estimate(calculate_heuristic)
                current_node = min_estimate

            if current_node is None:
                print("Path does not exist!")
                return None

            if current_node == end:
                reconstructed_path: list = []

                while parents[current_node] != current_node:
                    reconstructed_path.append(current_node)
                    current_node = parents[current_node]

                reconstructed_path.append(start)
                reconstructed_path.reverse()

                return reconstructed_path, self.get_path_cost_by_name(reconstructed_path)

            for (neighbor, weight) in self.get_node_neighbours_by_name(current_node):

                if neighbor not in open_list and neighbor not in closed_list:
                    open_list.add(neighbor)
                    parents[neighbor] = current_node
                    from_start_dist[neighbor] = from_start_dist[current_node] + weight

                else:
                    if from_start_dist[neighbor] > from_start_dist[current_node] + weight:
                        from_start_dist[neighbor] = from_start_dist[current_node] + weight
                        parents[neighbor] = current_node

                        if neighbor in closed_list:
                            closed_list.remove(neighbor)
                            open_list.add(neighbor)

            open_list.remove(current_node)
            closed_list.add(current_node)

            print("Path does not exist!")
            return None
