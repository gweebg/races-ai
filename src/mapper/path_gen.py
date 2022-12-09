import copy
import math
from collections import deque

from rich.console import Console

from src.graph.graph import Graph
from src.parser.parser import MapPiece

from src.models.race_car import RaceCar, Coordinates

console = Console()


class CircuitNode:
    def __init__(self, car: RaceCar, piece: MapPiece):
        self.car = car
        self.piece = piece

    def __hash__(self):
        return hash(self.car) + hash(self.piece)

    def __eq__(self, other):
        return (self.car == other.car) and (self.piece == other.piece)


def is_out_of_bounds(car: RaceCar, circuit_x: int, circuit_y: int) -> bool:
    if (0 <= car.pos.x < circuit_x) and (0 <= car.pos.y < circuit_y):
        return False

    return True


def calc_distance_heur(pos1: tuple[int, int], pos_list: list[tuple[int, int]]) -> float:
    lesser = None

    for tup in pos_list:
        curr = math.sqrt((tup[0] - pos1[0]) ** 2 + (tup[1] - pos1[1]) ** 2)
        if lesser is None or curr < lesser:
            lesser = curr

    return lesser


def calc_manhatten_dist_heur(pos1: tuple[int, int], pos_list: list[tuple[int, int]]) -> int:
    lesser = None

    for pos2 in pos_list:
        curr = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
        if lesser is None or curr < lesser:
            lesser = curr

    return lesser


def calc_heur(node: CircuitNode, finish_pos_list: list[tuple[int, int]]) -> float:
    if node.piece is MapPiece.FINISH:
        return 0
    elif node.piece is MapPiece.OUTSIDE_TRACK:
        return 1_000_000

    return calc_manhatten_dist_heur((node.car.pos.x, node.car.pos.y), finish_pos_list)


def generate_paths_graph(circuit: list[list[MapPiece]], init_pos_x: int, init_pos_y: int,
                         finish_pos_list: list[tuple[int, int]]) -> Graph:
    graph = Graph(True)

    car = RaceCar(
        pos=Coordinates(x=init_pos_x, y=init_pos_y)
    )

    start_node = CircuitNode(car, circuit[init_pos_y][init_pos_x])

    # Queue with the nodes being processed.
    open_queue = deque()
    open_queue.append(start_node)

    # Set of nodes already expanded.
    closed_set = set()

    while len(open_queue) > 0:

        node: CircuitNode = open_queue.popleft()

        if node in closed_set:
            continue

        next_node_paths = expand_track_moves(circuit, node)

        for (start_node, last_node, node_crashed, crash_node) in next_node_paths:

            if last_node.piece == MapPiece.FINISH:
                last_node.car.set_acc_zero()
                last_node.car.set_vel_zero()

            if crash_node is not None:
                graph.add_edge(node, crash_node, 25)
                graph.add_edge(crash_node, last_node, 0)

            else:
                graph.add_edge(node, last_node, 1)

            if last_node not in closed_set and last_node.piece is not MapPiece.FINISH:
                open_queue.append(last_node)

        closed_set.add(node)

    set_heuristics(graph, finish_pos_list)

    return graph


def set_heuristics(graph: Graph, finish_pos_list: list[tuple[int, int]]):
    for node in graph.graph.keys():
        graph.heur[node] = calc_heur(node, finish_pos_list)


def get_node_path(circuit: list[list[MapPiece]], node: CircuitNode):
    n_x: int = node.car.pos.x
    n_y: int = node.car.pos.y

    end_x: int = n_x + node.car.vel.x
    end_y: int = n_y + node.car.vel.y

    x_dir: int = max(-1, min(end_x - n_x, 1))
    y_dir: int = max(-1, min(end_y - n_y, 1))

    last_node: CircuitNode = copy.deepcopy(node)

    while n_x != end_x or n_y != end_y:

        if n_x != end_x:
            n_x += x_dir

        if n_y != end_y:
            n_y += y_dir

        if (n_x >= len(circuit[0])) or (n_x < 0) or (n_y >= len(circuit)) or (n_y < 0):
            return last_node, True, None

        if circuit[n_y][n_x] is MapPiece.OUTSIDE_TRACK:
            n_node = copy.deepcopy(last_node)
            n_node.piece = circuit[n_y][n_x]

            n_node.car.pos.x = n_x
            n_node.car.pos.y = n_y

            last_node.car.set_vel_zero()
            last_node.car.set_acc_zero()

            return last_node, True, n_node

        if circuit[n_y][n_x] is MapPiece.FINISH:
            last_node.piece = circuit[n_y][n_x]

            last_node.car.pos.x = n_x
            last_node.car.pos.y = n_y

            return last_node, False, None

        last_node.car.pos.x = n_x
        last_node.car.pos.y = n_y
        last_node.piece = circuit[n_y][n_x]

    return last_node, False, None


def expand_track_moves(circuit: list[list[MapPiece]], circuit_node: CircuitNode):
    list_paths = []

    if circuit_node.piece is MapPiece.FINISH:
        return list_paths

    closed_set = set()

    # Up #

    node = copy.deepcopy(circuit_node)
    node.car.accel_up()
    node.car.update_vel()

    last_node, is_crashed, crash_node = get_node_path(circuit, node)

    if last_node not in closed_set:
        closed_set.add(last_node)
        list_paths.append((node, last_node, is_crashed, crash_node))

    # Down #

    node = copy.deepcopy(circuit_node)
    node.car.accel_down()
    node.car.update_vel()

    last_node, is_crashed, crash_node = get_node_path(circuit, node)

    if last_node not in closed_set:
        closed_set.add(last_node)
        list_paths.append((node, last_node, is_crashed, crash_node))

    # Left #

    node = copy.deepcopy(circuit_node)
    node.car.accel_left()
    node.car.update_vel()

    last_node, is_crashed, crash_node = get_node_path(circuit, node)

    if last_node not in closed_set:
        closed_set.add(last_node)
        list_paths.append((node, last_node, is_crashed, crash_node))

    # Right #

    node = copy.deepcopy(circuit_node)
    node.car.accel_right()
    node.car.update_vel()

    last_node, is_crashed, crash_node = get_node_path(circuit, node)

    if last_node not in closed_set:
        closed_set.add(last_node)
        list_paths.append((node, last_node, is_crashed, crash_node))

    # Top-Right #

    node = copy.deepcopy(circuit_node)
    node.car.accel_top_right()
    node.car.update_vel()

    last_node, is_crashed, crash_node = get_node_path(circuit, node)

    if last_node not in closed_set:
        closed_set.add(last_node)
        list_paths.append((node, last_node, is_crashed, crash_node))

    # Top-Left #

    node = copy.deepcopy(circuit_node)
    node.car.accel_top_left()
    node.car.update_vel()

    last_node, is_crashed, crash_node = get_node_path(circuit, node)

    if last_node not in closed_set:
        closed_set.add(last_node)
        list_paths.append((node, last_node, is_crashed, crash_node))

    # Down-Right #

    node = copy.deepcopy(circuit_node)
    node.car.accel_down_right()
    node.car.update_vel()

    last_node, is_crashed, crash_node = get_node_path(circuit, node)

    if last_node not in closed_set:
        closed_set.add(last_node)
        list_paths.append((node, last_node, is_crashed, crash_node))

    # Down-Left #

    node = copy.deepcopy(circuit_node)
    node.car.accel_down_left()
    node.car.update_vel()

    last_node, is_crashed, crash_node = get_node_path(circuit, node)

    if last_node not in closed_set:
        closed_set.add(last_node)
        list_paths.append((node, last_node, is_crashed, crash_node))

    # Middle #

    node = copy.deepcopy(circuit_node)
    node.car.update_vel()

    last_node, is_crashed, crash_node = get_node_path(circuit, node)

    if last_node not in closed_set:
        closed_set.add(last_node)
        list_paths.append((node, last_node, is_crashed, crash_node))

    return list_paths
