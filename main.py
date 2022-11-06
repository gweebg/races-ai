from graph.basegraph import BaseGraph
from graph.node import Node


def main():
    graph = BaseGraph()

    graph.add_edge(Node("Elvas"), Node("Borba"), 15)
    graph.add_edge(Node("Borba"), Node("Estremoz"), 15)
    graph.add_edge(Node("Estremoz"), Node("Evora"), 40)
    graph.add_edge(Node("Evora"), Node("Montemor"), 20)
    graph.add_edge(Node("Montemor"), Node("Vendas Novas"), 15)
    graph.add_edge(Node("Vendas Novas"), Node("Lisboa"), 50)
    graph.add_edge(Node("Elvas"), Node("Arraiolos"), 50)
    graph.add_edge(Node("Arraiolos"), Node("Elvas"), 90)

    print(graph.edges_as_text())
    graph.draw()


if __name__ == '__main__':
    SystemExit(main())
