from typing import Callable, Optional

from src.mapper.path_gen import generate_paths_graph, CircuitNode
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
        self.graph: tuple[Graph, CircuitNode, list[CircuitNode]] = self.build_graph(self.map)

        self.algorithm_map: dict[str, Callable[[CircuitNode, list[CircuitNode]], Optional[tuple[list, int]]]] = {
            "DFS": self.graph[0].dfs_search,
            "BFS": self.graph[0].bfs_search,
            "Greedy": self.graph[0].greedy_search,
            "A*": self.graph[0].a_star_search
        }

    @staticmethod
    def build_graph(map_path: str) -> tuple[Graph, CircuitNode, list[CircuitNode]]:
        """
        Given the path to a map, this method generates the corresponding graph.
        This graph contains every possible play in the game, for every position.

        :param map_path: Map path.
        """

        circuit, start_pos, finish_pos_list = parse_map(map_path)

        graph, closed_set = generate_paths_graph(circuit, start_pos[0], start_pos[1], finish_pos_list)

        starting_node = CircuitNode(
            RaceCar(pos=Coordinates(x=start_pos[0], y=start_pos[1])),
            circuit[start_pos[1]][start_pos[0]]
        )

        finish_nodes: list[CircuitNode] = list(map(
            lambda pos:
            CircuitNode(RaceCar(pos=Coordinates(x=pos[0], y=pos[1])), circuit[pos[1]][pos[0]]),
            finish_pos_list
        ))

        return graph, starting_node, finish_nodes

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

        # Getting the result path and cost.
        self.path, self.cost = algorithm_func(self.graph[1], self.graph[2])

        # Cleaning up the path to only get the plays and not every node visited.
        tuple_path = self.path_to_tuple(self.path)

        # Running the simulation.
        # Simulation(self.tile_map, tuple_path).simulate()
        return tuple_path, self.cost, self.tile_map
