from Structures.Arc import Arc
from Structures.Vertex import Vertex


class CircleEvent:
    def __init__(self, alpha: Arc, center: Vertex, value: float):
        super().__init__()
        self.alpha = alpha
        self.circ_center = center
        self.value = value
