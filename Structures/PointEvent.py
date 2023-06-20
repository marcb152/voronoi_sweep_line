from Structures.Event import Event
from Structures.Vertex import Vertex


class PointEvent(Event):
    def __init__(self, vertex: Vertex):
        super().__init__()
        self.vertex = vertex
        self.value = vertex.y
