from Vertex import Vertex

class Arc:
    def __init__(self, vert: Vertex):
        """
        This type defines a parabola.
        :param vert: The vertex linked to this parabola
        """
        self.vertex = None
        self.circle_event = None
        self.right_arc = None
        self.left_arc = None

    def lower_bound(self) -> float:
        """
        Calculates the lower bound of the arc, x-coord-wise.
        :return: The lower intersection with another arc, if any.
        Defaults to -10 000 if none is found.
        """
        #TODO
        pass

    def upper_bound(self) -> float:
        """
        Calculates the upper bound of the arc, x-coord-wise.
        :return: The upper intersection with another arc, if any.
        Defaults to +10 000 if none is found.
        """
        #TODO
        pass

    def is_within_bounds(self, x: float):
        if self.lower_bound() <= x <= self.upper_bound():
            return True
        else:
            return False

    @staticmethod
    def calculate_intersection(left_arc, right_arc) -> Vertex | None:
        """
        Calculates the intersection point between 2 arcs.
        :param left_arc: The first arc, must be of type Arc.
        :param right_arc: The second arc, must be of type Arc.
        :return: A point if found, otherwise None.
        """
        #TODO
        intersection_vert = Vertex()
        return intersection_vert
