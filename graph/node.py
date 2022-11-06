class Node:
    """
    Represent a node in a graph.
    Each node has a name, id (optional) and heuristic value (optional).
    """

    def __init__(self, name: str, node_heuristic: int = -1, node_id: int = -1):
        self.id = node_id
        self.heuristic = node_heuristic
        self.name = name

    def __repr__(self):
        return f'Node(id = {self.id}, name = {self.name}, h = {self.heuristic})'

    def __str__(self):
        return f'Node(id = {self.id}, name = {self.name}, heuristic = {self.heuristic})'

    def __eq__(self, other: 'Node'):
        # Two nodes are the same if their name is the same.
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
