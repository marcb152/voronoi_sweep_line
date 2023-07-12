from Structures.Vertex import Vertex


class Edge:
    def __init__(self, vert0: Vertex = None, vert1: Vertex = None):
        self.points = [vert0, vert1]
        self.previous = None
        self.next = None
        self.face = 0
        self.twin = None
        self.origin = None
