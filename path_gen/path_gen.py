from graph.graph import Graph
from parser.parser import MapPiece
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

        return self.pos_x == other.pos_x and self.pos_y == other.pos_y \
               and self.vel_x == other.vel_x and self.vel_y == other.vel_y \
               and self.accel_x == other.accel_x and self.accel_y == other.accel_y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.pos_x + self.pos_y + self.vel_x + self.vel_y + self.accel_x + self.accel_y)

    def update(self):
        self.vel_x += self.accel_x
        self.vel_y += self.accel_y
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y

    def update_vel(self):
        self.vel_x += self.accel_x
        self.vel_y += self.accel_y

    def accel_up(self):
        self.accel_y = self.accel_y - 1 if self.accel_y > -1 else self.accel_y

    def accel_down(self):
        self.accel_y = self.accel_y + 1 if self.accel_y < 1 else self.accel_y

    def accel_left(self):
        self.accel_x = self.accel_x - 1 if self.accel_x > -1 else self.accel_x

    def accel_right(self):
        self.accel_x = self.accel_x + 1 if self.accel_x < 1 else self.accel_x

    def accel_topleft(self):
        self.accel_up()
        self.accel_left()

    def accel_topright(self):
        self.accel_up()
        self.accel_right()

    def accel_downleft(self):
        self.accel_down()
        self.accel_left()

    def accel_downright(self):
        self.accel_down()
        self.accel_right()


class CircuitNode:
    car: Car
    piece: MapPiece

    def __init__(self, car, piece):
        self.car = car
        self.piece = piece

    def __hash__(self):
        a = hash(self.car) + hash(self.piece)
        return a

    def __eq__(self, other):
        if self is other:
            return True
        return self.car == other.car and self.piece == other.piece


def is_out_of_bounds(car, circuit_x, circuit_y):
    if 0 <= car.pos_x < circuit_x and 0 <= car.pos_y < circuit_y:
        return False
    else:
        return True


def generate_player_graph(circuit, init_pos_x, init_pos_y):
    g = Graph(True)
    car = Car(pos_x=init_pos_x, pos_y=init_pos_y)
    start_node = CircuitNode(car, circuit[init_pos_x][init_pos_y])
    open_list = [start_node]
    closed_set = set()

    while len(open_list) > 0:
        #  print("open_list: ", len(open_list), " closed_set: ", len(closed_set))
        node = open_list.pop()
        if node in closed_set:
            continue

        next_node_paths = expand_track_moves(circuit, node)

        for (start_node, last_node, is_crashed, crash_node) in next_node_paths:
            cost = 25 if is_crashed else 1
            g.add_edge(node, start_node, cost)
            if crash_node is not None:
                g.add_edge(start_node, crash_node, 0)
                g.add_edge(crash_node, last_node, 0)
            else:
                g.add_edge(start_node, last_node, 0)

            if last_node not in closed_set:
                open_list.append(last_node)

        closed_set.add(node)

    return g


# returns end node, if it crashed, crash node
def get_node_path(circuit, node):
    nx = node.car.pos_x
    ny = node.car.pos_y
    endx = nx + node.car.vel_x
    endy = ny + node.car.vel_y
    xdir = max(-1, min(endx - nx, 1))
    ydir = max(-1, min(endy - ny, 1))
    last_node = copy.deepcopy(node)

    while nx != endx or ny != endy:
        if nx != endx:
            nx += xdir
        if ny != endy:
            ny += ydir

        if nx >= len(circuit[0]) or nx < 0 or ny >= len(circuit) or ny < 0:
            return last_node, True, None

        if circuit[ny][nx] is MapPiece.OUTSIDE_TRACK:
            n_node = copy.deepcopy(last_node)
            n_node.piece = circuit[ny][nx]
            n_node.car.pos_x = nx
            n_node.car.pos_y = ny
            last_node.car.vel_x = 0
            last_node.car.vel_y = 0
            last_node.car.accel_x = 0
            last_node.car.accel_y = 0
            return last_node, True, n_node

        if circuit[ny][nx] is MapPiece.FINISH:
            last_node.piece = circuit[ny][nx]
            last_node.car.pos_x = nx
            last_node.car.pos_y = ny
            return last_node, False, None

        last_node.car.pos_x = nx
        last_node.car.pos_y = ny
        last_node.car.piece = circuit[ny][nx]

    return last_node, False, None


def expand_track_moves(circuit, c_node: CircuitNode):
    list_paths = []

    node = copy.deepcopy(c_node)
    node.car.accel_up()
    node.car.update_vel()
    last_node, is_crashed, crash_node = get_node_path(circuit, node)
    list_paths.append((node, last_node, is_crashed, crash_node))

    node = copy.deepcopy(c_node)
    node.car.accel_down()
    node.car.update_vel()
    last_node, is_crashed, crash_node = get_node_path(circuit, node)
    list_paths.append((node, last_node, is_crashed, crash_node))

    node = copy.deepcopy(c_node)
    node.car.accel_left()
    node.car.update_vel()
    last_node, is_crashed, crash_node = get_node_path(circuit, node)
    list_paths.append((node, last_node, is_crashed, crash_node))

    node = copy.deepcopy(c_node)
    node.car.accel_right()
    node.car.update_vel()
    last_node, is_crashed, crash_node = get_node_path(circuit, node)
    list_paths.append((node, last_node, is_crashed, crash_node))

    node = copy.deepcopy(c_node)
    node.car.accel_topright()
    node.car.update_vel()
    last_node, is_crashed, crash_node = get_node_path(circuit, node)
    list_paths.append((node, last_node, is_crashed, crash_node))

    node = copy.deepcopy(c_node)
    node.car.accel_topleft()
    node.car.update_vel()
    last_node, is_crashed, crash_node = get_node_path(circuit, node)
    list_paths.append((node, last_node, is_crashed, crash_node))

    node = copy.deepcopy(c_node)
    node.car.accel_downright()
    node.car.update_vel()
    last_node, is_crashed, crash_node = get_node_path(circuit, node)
    list_paths.append((node, last_node, is_crashed, crash_node))

    node = copy.deepcopy(c_node)
    node.car.accel_downleft()
    node.car.update_vel()
    last_node, is_crashed, crash_node = get_node_path(circuit, node)
    list_paths.append((node, last_node, is_crashed, crash_node))

    return list_paths

def get_node_path_old(circuit, node):
    nlist = [node]
    nx = node.car.pos_x
    ny = node.car.pos_y
    endx = nx + node.car.vel_x
    endy = ny + node.car.vel_y
    xdir = max(-1, min(endx - nx, 1))
    ydir = max(-1, min(endy - ny, 1))

    while nx != endx or ny != endy:
        if nx != endx:
            nx += xdir
        if ny != endy:
            ny += ydir

        if nx >= len(circuit[0]) or nx < 0 or ny >= len(circuit) or ny < 0:
            return nlist, True

        if circuit[ny][nx] is MapPiece.OUTSIDE_TRACK:
            n_node = copy.deepcopy(node)
            n_node.piece = circuit[ny][nx]
            n_node.pos_x = nx
            n_node.pos_y = ny
            nlist.append(n_node)
            last_node = copy.deepcopy(nlist[-1])
            last_node.car.vel_x = 0
            last_node.car.vel_y = 0
            last_node.car.accel_x = 0
            last_node.car.accel_y = 0
            nlist.append(last_node)
            return nlist, True

        n_node = copy.deepcopy(node)
        n_node.piece = circuit[ny][nx]
        n_node.pos_x = nx
        n_node.pos_y = ny
        nlist.append(n_node)

    return nlist, False
