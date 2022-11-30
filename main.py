from graph.graph import Graph
from parser.parser import parse_map
from path_gen.path_gen import generate_player_graph, CircuitNode, Car


def compare_circuit_nodes(val1, val2):
    return val1.car.pos_x == val2.car.pos_x and val1.car.pos_y == val2.car.pos_y


def main():
    circuit, start_pos, finish_pos_list = parse_map("map_a.txt")
    graph = generate_player_graph(circuit, start_pos[0], start_pos[1])
    st = CircuitNode(Car(pos_x=start_pos[0], pos_y=start_pos[1]), circuit[start_pos[1]][start_pos[0]])
    f_pos = finish_pos_list[2]
    end = CircuitNode(Car(pos_x=f_pos[0], pos_y=f_pos[1]), circuit[f_pos[1]][f_pos[0]])
    path, cost = graph.dfs(st, end, compare_circuit_nodes)
    print(path)


if __name__ == '__main__':
    SystemExit(main())
