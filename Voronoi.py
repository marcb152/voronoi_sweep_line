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
                self._handle_point_event(p)
            elif type(p) == CircleEvent:
                self._handle_circle_event(p)
        # TODO: Manage all the unbounded arcs in 'tree'
        # |-> Calculate the intersection between them and the bounding box

    def _handle_point_event(self, pt_event: PointEvent):
        p = pt_event.vertex
        # We retrieve alpha, the arc above p
        alpha = self.tree.search_arc_above_vert(p)
        # We remove any circle event related to alpha
        # since it became obsolete after this point event
        if alpha.circle_events and len(alpha.circle_events) > 0:
            for c_event in alpha.circle_events:
                self.queue.remove(c_event)
                # Helping the Garbage Collector
                del c_event
            alpha.circle_events = None
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
        # Removing alpha from the tree
        parent_node_alpha = self.tree.find(alpha).root_node
        self.tree.find_and_remove(alpha)
        # Defining new arcs
        alpha0 = Arc(q, left_arc=alpha.left_arc)
        alpha1 = Arc(p)
        alpha2 = Arc(q, right_arc=alpha.right_arc)
        alpha0.right_arc = alpha1
        alpha1.left_arc = alpha0
        alpha1.right_arc = alpha2
        alpha2.left_arc = alpha1
        # Defining new tree nodes
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
        if alpha0.left_arc:
            center = Vertex.calculate_circumcenter(
                alpha0.left_arc.vertex,
                q,
                p)
            # Alpha0 is the arc that will disappear with this event
            circle_event = CircleEvent(alpha0, center)
            alpha0.circle_events.append(circle_event)
            alpha1.circle_events.append(circle_event)
            alpha0.left_arc.circle_events.append(circle_event)
            self.queue.insert(circle_event)
        if alpha2.right_arc:
            center = Vertex.calculate_circumcenter(
                alpha2.right_arc.vertex,
                q,
                p)
            # Alpha2 is the arc that will disappear with this event
            circle_event = CircleEvent(alpha2, center)
            alpha2.circle_events.append(circle_event)
            alpha1.circle_events.append(circle_event)
            alpha2.right_arc.circle_events.append(circle_event)
            self.queue.insert(circle_event)

    def _handle_circle_event(self, circle_event: CircleEvent):
        alpha = circle_event.alpha
        """
        What we have before:
                 p-alpha
                /       \
        q-alpha_left    r-alpha_right
        
        What we will obtain??
        """
        self.tree.find_and_remove(alpha)
        # TODO: delete alpha and handle breakpoints
        # We remove any circle event related to alpha
        # since it became obsolete after this point event
        if alpha.circle_events and len(alpha.circle_events) > 0:
            for c_event in alpha.circle_events:
                self.queue.remove(c_event)
                # Helping the Garbage Collector
                del c_event
            alpha.circle_events = None
        # We add the edges and vertices to the DCEL
        vertex = Arc.calculate_intersection(alpha.left_arc, alpha.right_arc)
        self.voronoi_graph.add_vertex(vertex)
        self.voronoi_graph.add_edge(Edge(vertex))
        # TODO

    def check_for_circle_events(self):
        pass
