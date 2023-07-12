import math


class Vertex:
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"{self.x, self.y}"

    # __init__ as defined
    @staticmethod
    def calculate_circumcenter(a: 'Vertex', b: 'Vertex', c: 'Vertex')\
            -> 'Vertex':
        """
        Formula based on wikipedia
        Source: https://en.wikipedia.org/wiki/Circumscribed_circle
        :param a: The first focus
        :param b: The second focus
        :param c: The third focus
        :return: The focus of the circumcenter
        """
        d = 2 * (a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y))
        u_x = ((a.x ** 2 + a.y ** 2) * (b.y - c.y)
               + (b.x ** 2 + b.y ** 2) * (c.y - a.y)
               + (c.x ** 2 + c.y ** 2) * (a.y - b.y))
        u_y = ((a.x ** 2 + a.y ** 2) * (c.x - b.x)
               + (b.x ** 2 + b.y ** 2) * (a.x - c.x)
               + (c.x ** 2 + c.y ** 2) * (b.x - a.x))
        center = Vertex(u_x / d, u_y / d)
        return center

    @staticmethod
    def calculate_circumradius(center: 'Vertex', a: 'Vertex') -> float:
        """
        Formula based on wikipedia
        :param center: Center of the circumcircle
        :param a: One point on the circumcircle
        :return: The radius of the circumcircle
        """
        return math.sqrt((center.x - a.x) ** 2 + (center.y - a.y) ** 2)
