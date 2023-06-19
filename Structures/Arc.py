from CircleEvent import CircleEvent
from Vertex import Vertex


class Arc:
    def __init__(self, focus: Vertex = None,
                 directrix: float = 0,
                 circle_event: CircleEvent = None,
                 right_arc: 'Arc' = None,
                 left_arc: 'Arc' = None):
        """
        This type defines a parabola
        :param focus: The focus linked to this parabola
        :param circle_event: One circle event to link to
        :param right_arc: The arc on the right of it, if any
        :param left_arc: The arc on the left of it, if any
        """
        self.focus = focus
        self.directrix = directrix
        self.circle_events = [circle_event]
        self.right_arc = right_arc
        self.left_arc = left_arc

    def lower_bound(self) -> float:
        """
        Calculates the lower bound of the arc, x-coord-wise.
        :return: The lower intersection with the left arc, if any.
        Defaults to -10 000 if none is found.
        """
        intersect = Arc.calculate_intersection(self.left_arc, self)
        if intersect:
            return intersect.x
        else:
            return -10000.0

    def upper_bound(self) -> float:
        """
        Calculates the upper bound of the arc, x-coord-wise.
        :return: The upper intersection with the right arc, if any.
        Defaults to +10 000 if none is found.
        """
        intersect = Arc.calculate_intersection(self, self.right_arc)
        if intersect:
            return intersect.x
        else:
            return 10000.0

    # __init__ as defined
    @staticmethod
    def calculate_intersection(left_arc: 'Arc', right_arc: 'Arc')\
            -> Vertex | None:
        """
        Calculates the intersection point between 2 arcs
        :param left_arc: The first arc, must be of type Arc
        :param right_arc: The second arc, must be of type Arc
        :return: A point if found, otherwise None
        """
        # TODO
        intersection_vert = Vertex()
        return intersection_vert
