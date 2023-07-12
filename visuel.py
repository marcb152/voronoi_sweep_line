import tkinter as tk
from Structures.Vertex import Vertex

class Visuel:
    def __init__(self, points: list[Vertex]):
        self.points = points
        self.wnd = tk.Tk()
        self.wnd.title("Voronoi")
        self.longeur = 200
        self.hauteur = 200
        self.offset = 50
        self.wnd.geometry(str(self.longeur) + "x" + str(self.hauteur))
        self.wnd.resizable(width=False, height=False)
        self.cnv = tk.Canvas(self.wnd)
        self.cnv.place(relx=0, rely=0, relwidth=1, relheight=1)

        # on affiche tous les points dans le canva
        self.affichage_point()

    def affichage_point(self):
        for i in self.points:
            self.cnv.create_oval(i.x - 5 + self.offset,
                                 i.y - 5 + self.offset,
                                 i.x + 5 + self.offset,
                                 i.y + 5 + self.offset,
                                 fill="red")

    def trace(self, p1: Vertex, p2: Vertex):
        print("Trace")
        self.cnv.create_line(p1.x, p1.y, p2.x, p2.y, width=3)

    def trace1(self, p1: Vertex, p2: Vertex):
        self.cnv.create_line(p1.x, p1.y, p2.x, p2.y, width=3, fill="red")

    def hyperbola(self, focus: Vertex, directrix: float):
        hyperbola = []
        if focus.y == directrix:
            return
        for x in range(0, 100, 5):
            y = (((focus.x - x) ** 2 + focus.y ** 2 - directrix ** 2) /
                 (2 * (focus.y - directrix)))
            hyperbola.append((x + self.offset, y + self.offset))
        self.cnv.create_line(hyperbola, tags="hyperbola")
        self.cnv.update()

    def reset_hyperbolas(self):
        self.cnv.delete("hyperbola")

    # pointtriangle est sous la forme d'une double liste qui contient trois
    # point ex: [[4.2, 530.4], [61.8, 48.6], [82.2, 22.2]]
    def triangle(self, pointtriangle):
        for i in range(-1, 2):
            self.trace(pointtriangle[i][0], pointtriangle[i][1],
                       pointtriangle[i + 1][0], pointtriangle[i + 1][1])
