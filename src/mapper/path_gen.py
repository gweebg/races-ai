import copy
import math
import random
from collections import deque

from rich.console import Console

from src.graph.graph import Graph
from src.parser.parser import MapPiece

from src.models.race_car import RaceCar, Coordinates

from src.graph.imm_graph import ImmGraph, ImmGraphTransaction

console = Console()


class CircuitNode:
    def __init__(self, car: RaceCar, piece: MapPiece):
        self.car: RaceCar = car
        self.piece: MapPiece = piece
        self.gen: int = 0

    def __hash__(self):
        return hash(self.car) + hash(self.piece) + hash(self.gen)

    def __eq__(self, other):
        return (self.car == other.car) and (self.piece == other.piece) and (self.gen == other.gen)

    def __str__(self):
        return f"car:{self.car}; piece:{self.piece}; gen:{self.gen}"


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


def resolve_collisions(a_path_list: list[tuple[list[CircuitNode], int]], graph: Graph, finish_nodes: list[CircuitNode],
                       algorithm: str) -> list[tuple[list[CircuitNode], int]]:
    assert graph.is_directed
    immgraph_list = [ImmGraph.wrap_graph(graph) for i in range(len(a_path_list))]
    path_list = [path for path, cost in a_path_list]

    i = 0
    exit_b = False
    while not exit_b:
        inds = []
        for j in range(len(path_list)):
            if len(path_list[j]) > i + 1:
                inds.append(j)

        if len(inds) == 0:
            exit_b = True
            break

        pos_map = {}
        for j in inds:
            path = path_list[j]
            if path[i + 1].car.pos not in pos_map:
                pos_map[path[i + 1].car.pos] = path[i]
            else:
                igraph = immgraph_list[j]
                trans = ImmGraphTransaction()
                node = path[i]
                g_node = copy.deepcopy(node)
                g_node.gen += 1
                trans.add_val(g_node)
                trans.add_heur(g_node, igraph.get_heuristic(node))

                neighbors_to, neighbors_from = igraph.get_all_associated(node)
                for neigh, weight in neighbors_from:
                    trans.add_edge(neigh, g_node, weight)
                    trans.remove_edge(neigh, node)

                rem_pos_set = set()
                for neigh, weight in neighbors_to:
                    trans.add_edge(g_node, neigh, weight)
                    for k in inds:
                        if k == j:
                            continue
                        n_node = path_list[k][i + 1]
                        if n_node.car.pos == neigh.car.pos and n_node.car.pos not in rem_pos_set and node.piece != MapPiece.OUTSIDE_TRACK:
                            trans.remove_edge(node, neigh)
                            rem_pos_set.add(n_node.car.pos)

                igraph = igraph.apply_transaction(trans)
                s_path = None
                match algorithm:
                    case "DFS":
                        s_path, _ = igraph.dfs_search(node, finish_nodes)
                    case "BFS":
                        s_path, _ = igraph.bfs_search(node, finish_nodes)
                    case "A*":
                        s_path, _ = igraph.a_star_search(node, finish_nodes)
                    case "Greedy":
                        s_path, _ = igraph.greedy_search(node, finish_nodes)
                    case _:
                        raise RuntimeError(f"received unknown algo:{algorithm}")

                n_path = []

                for k in range(i):
                    n_path.append(path[k])

                n_path += s_path

                path_list[j] = n_path
                immgraph_list[j] = igraph

        i += 1

    ret_list = []
    for path in path_list:
        for node in path:
            node.gen = 0 if node.gen != 0 else node.gen
        weight = 0
        for i in range(1, len(path)):
            weight += graph.get_weight(path[i-1], path[i])
        ret_list.append((path, weight))
    return ret_list


def generate_paths_graph(circuit: list[list[MapPiece]], start_pos_list: list[tuple[int, int]],
                         finish_pos_list: list[tuple[int, int]], graph=None, closed_set=None) -> tuple[Graph, set]:
    if graph is None:
        graph = Graph(True)

    if closed_set is None:
        # Set of nodes already expanded.
        closed_set = set()

    # Queue with the nodes being processed.
    open_queue = deque()

    for start_pos in start_pos_list:
        start_node = CircuitNode(
            RaceCar(
                pos=Coordinates(x=start_pos[0], y=start_pos[1])
            ),
            circuit[start_pos[1]][start_pos[0]]
        )
        open_queue.append(start_node)

    while len(open_queue) > 0:

        node: CircuitNode = open_queue.popleft()

        if node in closed_set:
            continue

        next_node_paths = expand_track_moves(circuit, node)

        for (start_node, last_node, node_crashed, crash_node) in next_node_paths:

            last_node.car.set_acc_zero()
            if last_node.piece == MapPiece.FINISH:
                last_node.car.set_vel_zero()

            if crash_node is not None:
                crash_node.car.set_acc_zero()
                graph.add_edge(node, crash_node, 25)
                graph.add_edge(crash_node, last_node, 0)

            else:
                graph.add_edge(node, last_node, 1)

            if last_node not in closed_set and last_node.piece is not MapPiece.FINISH:
                open_queue.append(last_node)

        closed_set.add(node)

    set_heuristics(graph, finish_pos_list)

    return graph, closed_set


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
