from Event import Event
from Arc import Arc
from Vertex import Vertex


class CircleEvent(Event):
    def __init__(self, alpha: Arc, center: Vertex):
        super().__init__()
        self.alpha = alpha
        self.circ_center = center
        self.value = center.y
