import pytest

from graph.basegraph import BaseGraph
from graph.node import Node


node_list_1 = [Node("Elvas"), Node("Borba"), Node("Estremoz"), Node("Evora"), Node("Montemor"), Node("Vendas Novas"),
               Node("Lisboa")]


@pytest.fixture()
def graph_object():
    yield BaseGraph()


def test_dfs_search(graph_object):
    ...






