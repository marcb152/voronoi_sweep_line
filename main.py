from Voronoi import Voronoi
from Structures.Vertex import Vertex

if __name__ == '__main__':
    print("Hello world")
    points = [Vertex(15, 26), Vertex(65, 43), Vertex(2, 63), Vertex(94, 35)]
    voronoi = Voronoi(points)
    print(voronoi.voronoi_graph)
    # TODO: Generate points and call Voronoi(points)

# TODO LIST (GLOBAL):
# todo - understand how the DCEL is supposed to build itself -> by reference
# todo - fully comment the code
# todo - add credits/sources where required
