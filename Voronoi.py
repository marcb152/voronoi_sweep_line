from Structures.Vertex import Vertex
from Structures.DCEL import DCEL
from Structures.BSTNode import BSTNode
from Structures.PointEvent import PointEvent
from Structures.CircleEvent import CircleEvent
from Structures.Arc import Arc
from Structures.Edge import Edge
from Structures.PriorityQueue import PriorityQueue
from visuel import Visuel

from time import sleep


class Voronoi:
    def __init__(self, entry: list[Vertex], visuel: Visuel):
        self.visuel = visuel
        old_vertices = []
        self.tree = BSTNode(None)
        self.voronoi_graph = DCEL()
        # Converting points to list of PointEvents
        points = [PointEvent(vert) for vert in entry]
        points.sort()
        self.queue = PriorityQueue(points)
        while not self.queue.is_empty:
            for p in self.queue.pop_min():
                if type(p) == PointEvent:
                    print("Point event {}".format(p.vertex))
                    old_vertices.append(p.vertex)
                    self._handle_point_event(p)
                elif type(p) == CircleEvent:
                    print("Circle event {}".format(p.arc.focus))
                    self._handle_circle_event(p)
                # Visual update
                self.visuel.reset_hyperbolas()
                for vert in old_vertices:
                    self.visuel.hyperbola(vert, p.value)
                # Sleep for visual debug
                sleep(2)
        # TODO: Manage all the unbounded arcs in 'tree' -> EASY
        # |-> Calculate the intersection between them and the bounding box

    def _handle_point_event(self, pt_event: PointEvent):
        p = pt_event.vertex
        # We retrieve alpha, the arc above p
        alpha = self.tree.search_arc_above_vert(p, pt_event.value)
        # If alpha is None -> this is the first point of the graph
        if alpha is None:
            self.tree.arc = Arc(p)
            return
        # We remove any circle event related to alpha
        # since it became obsolete after this point event
        if alpha.circle_events and len(alpha.circle_events) > 0:
            for c_event in alpha.circle_events:
                if c_event:
                    self.queue.delete(c_event)
                    # Helping the Garbage Collector
                    del c_event
            alpha.circle_events = None
        # Let q be the focus linked to alpha
        q = alpha.focus
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
        
        What we will obtain because I'm lazy:
            p-alpha1
            /       \
        q-alpha0    q-alpha2
        """
        # Removing alpha from the tree
        parent_node_alpha = self.tree.find(alpha, pt_event.value).root_node
        self.tree.find_and_remove(alpha, pt_event.value)
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
        vert0 = Arc.calculate_intersection(alpha0, alpha1, pt_event.value)
        print(f"Intersection of point arc with focus {alpha0.focus} and "
              f"arc with focus {alpha1.focus} with directrix {pt_event.value}, "
              f"intersection at {vert0}")
        vert1 = Arc.calculate_intersection(alpha1, alpha2, pt_event.value)
        print(f"Intersection of point arc with focus {alpha1.focus} and "
              f"arc with focus {alpha2.focus} with directrix {pt_event.value}, "
              f"intersection at {vert1}")
        self.voronoi_graph.add_edge(Edge(vert0, vert1))
        if vert0 and vert1:
            self.visuel.trace(vert0, vert1)
        # Check for circle events on the left and on the right
        self.check_for_circle_events(alpha0.left_arc, alpha0, alpha1)
        self.check_for_circle_events(alpha1, alpha2, alpha2.right_arc)

    def _handle_circle_event(self, circle_event: CircleEvent):
        alpha = circle_event.alpha
        alpha_left = alpha.left_arc
        alpha_right = alpha.right_arc
        """
        What we have before:
                 p-alpha
                /       \
        q-alpha_left    r-alpha_right
        
        What we will obtain??
        """
        self.tree.find_and_remove(alpha, circle_event.value)
        # TODO: delete alpha and handle breakpoints
        # We remove any circle event related to alpha
        # since it became obsolete after this point event
        if alpha.circle_events and len(alpha.circle_events) > 0:
            for c_event in alpha.circle_events:
                self.queue.delete(c_event)
                # Helping the Garbage Collector
                del c_event
            alpha.circle_events = None
        # We add the edges and vertices to the DCEL
        vertex = Arc.calculate_intersection(alpha.left_arc,
                                            alpha.right_arc,
                                            circle_event.value)
        self.voronoi_graph.add_vertex(vertex)
        self.voronoi_graph.add_edge(Edge(vertex))
        # Check for circle events on the left and on the right
        self.check_for_circle_events(
            alpha_left.left_arc,
            alpha_left,
            alpha_right)
        self.check_for_circle_events(
            alpha_left,
            alpha_right,
            alpha_right.right_arc)

    def check_for_circle_events(self, alpha_left: Arc,
                                alpha: Arc,
                                alpha_right: Arc):
        """
        This function checks for circle events on the left and on the right of
        these 3 arcs
        :param alpha_left: The left arc
        :param alpha: The middle arc
        :param alpha_right: The right arc
        """
        """
        Graph overview:
                 p-alpha
                /       \
        q-alpha_left    r-alpha_right
        """
        if alpha_left and alpha and alpha_right:
            q = alpha_left.focus
            p = alpha.focus
            r = alpha_right.focus
            center = Vertex.calculate_circumcenter(q, p, r)
            radius = Vertex.calculate_circumradius(center, p)
            # alpha is the arc that will disappear with this event
            circle_event = CircleEvent(alpha, center, center.y + radius)
            # Referencing
            alpha_left.circle_events.append(circle_event)
            alpha.circle_events.append(circle_event)
            alpha_right.circle_events.append(circle_event)
            self.queue.insert(circle_event)
