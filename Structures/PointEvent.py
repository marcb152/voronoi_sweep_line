from Event import Event
from Vertex import Vertex

class PointEvent(Event):
    def __init__(self, vertex: Vertex):
        super().__init__()
        self.vertex = vertex