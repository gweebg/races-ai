from graph.searchgraph import SearchGraph
from enum import Enum
from graph.node import Node
import copy


class Car:
    pos_x = 0
    pos_y = 0
    vel_x = 0
    vel_y = 0
    accel_x = 0
    accel_y = 0

    def __init__(self, pos_x=0, pos_y=0, vel_x=0, vel_y=0, accel_x=0, accel_y=0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.accel_x = accel_x
        self.accel_y = accel_y

    def __eq__(self, other):
        if self is other:
            return True

        return self.pos_x == other.pos_y and self.pos_y == other.pos_y \
               and self.vel_x == other.vel_x and self.vel_y == other.vel_y \
               and self.accel_x == other.accel_x and self.accel_y == other.accel_y

    def __ne__(self, other):
        return not self.__eq__(other)

    def update(self):
        self.vel_x += self.accel_x
        self.vel_y += self.accel_y
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y

    def accel_up(self):
        self.accel_y = self.accel_y + 1 if self.accel_y < 1 else self.accel_y
        self.update()

    def accel_down(self):
        self.accel_y = self.accel_y - 1 if self.accel_y > -1 else self.accel_y
        self.update()

    def accel_left(self):
        self.accel_x = self.accel_x + 1 if self.accel_x < 1 else self.accel_x
        self.update()

    def accel_right(self):
        self.accel_y = self.accel_x + 1 if self.accel_x > -1 else self.accel_x
        self.update()


class Piece(Enum):
    TRACK = 0
    OUTSIDE_TRACK = 1
    INIT = 2
    END = 3

    def is_inside_track(self):
        match self:
            case Piece.TRACK, Piece.END, Piece.INIT:
                return True
            case _:
                return False

    def travel_cost(self, other):
        if other.is_inside_track():
            return 1
        else:
            return 25


class CircuitNode:
    car: Car
    piece: Piece

    def __init__(self, car, piece):
        self.car = car
        self.piece = piece


def is_out_of_bounds(car, circuit_x, circuit_y):
    if car.pos_x < circuit_x and car.pos_y < circuit_y:
        return False
    else:
        return True


def generate_player_graph(circuit, init_pos_x, init_pos_y):
    g = SearchGraph(True)
    car = Car(pos_x=init_pos_x, pos_y=init_pos_y)
    start_node = CircuitNode(car, circuit[init_pos_x][init_pos_y])
    open_list = [start_node]

    while len(open_list) > 0:
        node = open_list.pop()
        next_nodes = expand_track_moves(circuit, node)

        for n_node in next_nodes:
            cost = node.piece.travel_cost(n_node.piece)
            g.add_edge(Node(value=node), Node(value=n_node), cost)
            open_list.append(n_node)

            if not n_node.piece.is_inside_track():
                penalized_node = copy.deepcopy(node)
                penalized_node.car.vel_x = 0
                penalized_node.car.vel_y = 0
                cost = n_node.piece.travel_cost(penalized_node.piece)
                g.add_edge(Node(value=n_node), Node(value=penalized_node), cost)
                open_list.append(penalized_node)


def expand_track_moves(circuit, c_node: CircuitNode):
    asd = []

    start_car = copy.copy(c_node.car)

    node = copy.deepcopy(c_node)
    car = node.car
    car.accel_up()

    if not is_out_of_bounds(car, len(circuit[0]), len(circuit)):
        asd.append(node)

    node = copy.deepcopy(c_node)
    node.car.accel_down()

    if not is_out_of_bounds(node.car, len(circuit[0]), len(circuit)):
        asd.append(node)

    node = copy.deepcopy(c_node)
    node.car.accel_left()

    if not is_out_of_bounds(node.car, len(circuit[0]), len(circuit)):
        asd.append(node)

    node = copy.deepcopy(c_node)
    node.car.accel_right()

    if not is_out_of_bounds(node.car, len(circuit[0]), len(circuit)):
        asd.append(node)

    node = copy.deepcopy(c_node)
    car.update()

    if not is_out_of_bounds(node.car, len(circuit[0]), len(circuit)) and node.car != start_car:
        asd.append(node)

    return asd
