import math

from Structures.Vertex import Vertex


class Arc:
    def __init__(self, focus: Vertex = None,
                 directrix: float = 0,
                 circle_event: 'CircleEvent' = None,
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

    def lower_bound(self, directrix: float) -> float:
        """
        Calculates the lower bound of the arc, x-coord-wise.
        :return: The lower intersection with the left arc, if any.
        Defaults to -10 000 if none is found.
        """
        intersect = Arc.calculate_intersection(self.left_arc, self, directrix)
        if intersect:
            return intersect.x
        else:
            return -10000.0

    def upper_bound(self, directrix: float) -> float:
        """
        Calculates the upper bound of the arc, x-coord-wise.
        :return: The upper intersection with the right arc, if any.
        Defaults to +10 000 if none is found.
        """
        intersect = Arc.calculate_intersection(self, self.right_arc, directrix)
        if intersect:
            return intersect.x
        else:
            return 10000.0

    # __init__ as defined
    @staticmethod
    def calculate_intersection(left_arc: 'Arc', right_arc: 'Arc',
                               directrix: float) -> Vertex | None:
        """
        Calculates the intersection point between 2 arcs
        :param directrix:
        :param left_arc: The first arc, must be of type Arc
        :param right_arc: The second arc, must be of type Arc
        :return: A point if found, otherwise None
        """
        # We verify if both arcs are not null
        if left_arc is None or right_arc is None:
            return None
        # Variables
        x, y = 0.0, 0.0
        f0 = left_arc.focus
        f1 = right_arc.focus
        # Calculating second order constants: ax²+bx+c=0
        if directrix - f0.y == 0:
            # Division by zero avoidance
            return None
        a = (f1.y - f0.y) / (directrix - f0.y)
        b = (2 * f1.x - 2 * f0.x * (1 - (f0.y - f1.y) / (f0.y - directrix)))
        c = (f0.x ** 2 + f0.y ** 2 - f1.x ** 2 - f1.y ** 2 +
             (f1.y - f0.y) * (f0.x ** 2 + f0.y ** 2 - directrix ** 2) /
             (directrix - f0.y))
        # Calculating delta
        delta = b ** 2 - 4 * a * c
        # delta == 0 -> one solution only
        if delta == 0:
            x = - b / 2 * a
        # delta > 0 -> 2 solutions
        # We eliminate the one that is not bounded by the focus points
        elif delta > 0:
            x1 = (- b + math.sqrt(delta)) / 2 * a
            x2 = (- b - math.sqrt(delta)) / 2 * a
            solution_found = False
            # If x1 is bounded by the focus points, we keep it
            if f0.x <= x1 <= f1.x:
                x = x1
                solution_found = True
            # Elif x2 is bounded by the focus points, we keep it
            elif f0.x <= x2 <= f1.x:
                x = x2
                solution_found = True
            # If none of our values are bounded,
            # it means the left/right arcs were not in the supposed order
            # failure -> returns None
            if not solution_found:
                print("WARNING: You tried to calculate the intersection of two "
                      "arcs in the reversed left/right order!\n"
                      "The program will try to continue to execute, "
                      "it may yield incorrect results or crash. Be aware.")
                return None
        # delta < 0 -> no solutions
        elif delta < 0:
            return None
        # We calculate y based on our x result
        y = ((f0.x ** 2 - directrix ** 2 - 2 * x * f0.x + x ** 2 +
              f0.y ** 2) /
             (2 * (f0.y - directrix)))
        intersection_vert = Vertex(x, y)
        return intersection_vert
