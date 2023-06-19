from Vertex import Vertex


class Edge:
    def __init__(self, vert0: Vertex = None, vert1: Vertex = None):
        self.points = [vert0, vert1]
        self.previous = Edge()
        self.next = Edge()
        self.face = 0
        self.twin = Edge()
        self.origin = Vertex()
