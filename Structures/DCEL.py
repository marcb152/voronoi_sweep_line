from Structures.Edge import Edge
from Structures.Vertex import Vertex


class DCEL:
    def __init__(self):
        self.value = []

    def add_edge(self, edge: Edge):
        self.value.append(edge)

    def add_vertex(self, vert: Vertex):
        self.value.append(vert)
