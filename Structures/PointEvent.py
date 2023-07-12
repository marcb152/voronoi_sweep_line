from Structures.Vertex import Vertex


class PointEvent:
    def __init__(self, vertex: Vertex):
        super().__init__()
        self.vertex = vertex
        self.value = vertex.y

    def __str__(self) -> str:
        return f"{self.vertex}"

    def __lt__(self, other: 'PointEvent') -> bool:
        return self.vertex.y < other.vertex.y
