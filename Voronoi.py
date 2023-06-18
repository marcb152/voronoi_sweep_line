from Structures.Vertex import Vertex
from Structures.PriorityQueue import PriorityQueue
from Structures.DCEL import DCEL
from Structures.BSTNode import BSTNode
from Structures.PointEvent import PointEvent
from Structures.CircleEvent import CircleEvent
from Structures.Arc import Arc
from Structures.Edge import Edge

class Voronoi:
    def __init__(self, entry: list[Vertex]):
        self.tree = BSTNode(None)
        self.voronoi_graph = DCEL()
        self.queue = PriorityQueue(entry, max)
        while not self.queue.is_empty():
            p = self.queue.pop_max()
            if type(p) == PointEvent:
                self._handle_point_event(p.vertex)
            elif type(p) == CircleEvent:
                self._handle_circle_event(p.alpha)
        # TODO: Manage all the unbounded arcs in 'tree'
        # |-> Calculate the intersection between them and the bounding box

    def _handle_point_event(self, p: Vertex):
        # We retrieve alpha, the arc above p
        alpha = self.tree.search_arc_above_vert(p)
        # We remove any circle event related to alpha
        # since it became obsolete after this point event
        if alpha.circle_event:
            self.queue.remove(alpha.circle_event)
            del alpha.circle_event
        # Let q be the vertex linked to alpha
        q = alpha.vertex
        # We split alpha into alpha0 and alpha2
        # We create alpha1, the arc related to p
        """
        What we have before:
        q-alpha
        
        What we should obtain:
        intersection(alpha0, alpha1)-No arc
            /               \
        q-alpha0        intersect(alpha1, alpha2)-No arc
                            /               \
                        p-alpha1        q-alpha2
        
        What we will obtain:
            p-alpha1
            /       \
        q-alpha0    q-alpha2
        """
        parent_node_alpha = self.tree.find(alpha).root_node
        self.tree.find_and_remove(alpha)
        alpha0 = Arc(q)
        alpha1 = Arc(p)
        alpha2 = Arc(q)
        p_alpha1_node = BSTNode(alpha1, parent_node_alpha)
        q_alpha0_node = BSTNode(alpha0, p_alpha1_node)
        q_alpha2_node = BSTNode(alpha2, p_alpha1_node)
        p_alpha1_node.left_node = q_alpha0_node
        p_alpha1_node.right_node = q_alpha2_node
        # Add voronoi edges: intersection(alpha0, alpha1)
        # and intersection(alpha1, alpha2)
        vert0 = Arc.calculate_intersection(alpha0, alpha1)
        vert1 = Arc.calculate_intersection(alpha1, alpha2)
        self.voronoi_graph.add_edge(Edge(vert0, vert1))
        # Check for circle events on the left and on the right
        #TODO
        pass

    def _handle_circle_event(self, alpha: Arc):
        #TODO
        pass