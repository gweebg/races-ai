from typing import Callable, Optional

from src.mapper.path_gen import generate_paths_graph, CircuitNode, resolve_collisions
from src.mapper.simulation import Simulation
from src.mapper.tiles import TileMap

from src.models.race_car import RaceCar, Coordinates

from src.parser.parser import parse_map

from src.graph.graph import Graph


class Simulator:

    def __init__(self, map_path: str, algorithm: str, cars: int) -> None:

        self.map = map_path
        self.algorithm = algorithm
        self.cars = cars  # Todo #

        self.path = None
        self.cost = None

        self.tile_map = TileMap(self.map)
        self.graph, self.start_nodes, self.finish_nodes = self.build_graph(self.map)

        self.algorithm_map: dict[str, Callable[[CircuitNode, list[CircuitNode]], Optional[tuple[list, int]]]] = {
            "DFS": self.graph.dfs_search,
            "BFS": self.graph.bfs_search,
            "Greedy": self.graph.greedy_search,
            "A*": self.graph.a_star_search
        }

    @staticmethod
    def build_graph(map_path: str) -> tuple[Graph, list[CircuitNode], list[CircuitNode]]:
        """
        Given the path to a map, this method generates the corresponding graph.
        This graph contains every possible play in the game, for every position.

        :param map_path: Map path.
        """

        circuit, start_pos_list, finish_pos_list = parse_map(map_path)

        graph, closed_set = generate_paths_graph(circuit, start_pos_list, finish_pos_list)

        start_nodes: list[CircuitNode] = list(map(
            lambda pos:
            CircuitNode(RaceCar(pos=Coordinates(x=pos[0], y=pos[1])), circuit[pos[1]][pos[0]]),
            start_pos_list
        ))

        finish_nodes: list[CircuitNode] = list(map(
            lambda pos:
            CircuitNode(RaceCar(pos=Coordinates(x=pos[0], y=pos[1])), circuit[pos[1]][pos[0]]),
            finish_pos_list
        ))

        return graph, start_nodes, finish_nodes

    @staticmethod
    def path_to_tuple(path: list[CircuitNode]) -> list[tuple[int, int]]:
        """
        Converts a path in the for of list[CircuitNode] to a list
        of coordinates of type tuple[int, int].

        :param path: Path to be converted.
        """
        return [(node.car.pos.x + 1, node.car.pos.y + 1) for node in path]

    def get_resources(self):
        """
        Runs the simulation, first computes every data needed, such as
        graphs, paths and costs, then it displays the simulation using
        the Simulation class.
        """

        # Getting the text corresponding algorithm function.
        algorithm_func: Callable = self.algorithm_map.get(self.algorithm)

        s_node_iter = looping_range(len(self.start_nodes))
        s_node_paths = {}
        paths: list[tuple[list[CircuitNode], int]] = []

        for i in range(self.cars):
            s_node = self.start_nodes[next(s_node_iter)]
            if s_node in s_node_paths:
                path = s_node_paths[s_node]
            else:
                path = algorithm_func(s_node, self.finish_nodes)
                s_node_paths[s_node] = path
            paths.append(path)

        paths = resolve_collisions(paths, self.graph, self.finish_nodes, self.algorithm)

        tuple_paths: list[tuple[list[tuple[int, int]], int]] = []

        for path in paths:
            t_path = self.path_to_tuple(path[0])
            tuple_paths.append((t_path, path[1]))

        # Running the simulation.
        # Simulation(self.tile_map, tuple_path).simulate()
        return tuple_paths, self.tile_map


def looping_range(max_i: int = 0):
    it = 0
    while True:
        if it == max_i:
            it = 0
        yield it
        it += 1
