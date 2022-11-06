from graph.basegraph import BaseGraph
from graph.node import Node
from graph.searchgraph import SearchGraph


def main():
    graph = SearchGraph()

    graph.add_edge(Node("Elvas"), Node("Borba"), 15)
    graph.add_edge(Node("Borba"), Node("Estremoz"), 15)
    graph.add_edge(Node("Estremoz"), Node("Evora"), 40)
    graph.add_edge(Node("Evora"), Node("Montemor"), 20)
    graph.add_edge(Node("Montemor"), Node("Vendas Novas"), 15)
    graph.add_edge(Node("Vendas Novas"), Node("Lisboa"), 50)
    graph.add_edge(Node("Elvas"), Node("Arraiolos"), 50)
    graph.add_edge(Node("Arraiolos"), Node("Lisboa"), 90)

    # print(graph)
    # print(graph.get_edge_cost(Node("Elvas"), Node("Arraioklos")))
    # print(graph.get_path_cost([Node("Elvas"), Node("Arraiolos"), Node("Lisboa")]))
    print(graph.bfs_search("Elvas", "Lisboa"))

    graph.draw()


if __name__ == '__main__':
    SystemExit(main())
