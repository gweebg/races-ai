from graph.graph import Graph
from parser.parser import parse_map
from path_gen.path_gen import generate_player_graph, CircuitNode, Car

def main():
    circuit, start_pos, finish_pos_list = parse_map("map_a.txt")
    graph = generate_player_graph(circuit, start_pos[0], start_pos[1])
    print(graph)

if __name__ == '__main__':
    SystemExit(main())
