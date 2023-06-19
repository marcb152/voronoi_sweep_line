from Arc import Arc
from Vertex import Vertex


class BSTNode:
    def __init__(self, arc: Arc | None,
                 root_node: 'BSTNode' = None,
                 left_node: 'BSTNode' = None,
                 right_node: 'BSTNode' = None):
        """
        This class implements an x-coordinate sorted BST (left to right
        min to max X).
        :param arc:
        :param root_node: Must be of type BSTNode
        """
        self.root_node = root_node
        self.left_node = left_node
        self.right_node = right_node
        self.arc = arc

    def insert(self, arc: Arc):
        if self.arc is None:
            self.arc = arc
            pass

        if arc == self.arc:
            raise "NotImplementedException"
        elif arc.focus.x < self.arc.focus.x:
            if not self.left_node:
                self.left_node = BSTNode(arc, self)
            else:
                self.left_node.insert(arc)
        elif arc.focus.x > self.arc.focus.x:
            if not self.right_node:
                self.right_node = BSTNode(arc, self)
            else:
                self.right_node.insert(arc)
        else:
            raise "NotImplementedException"

    def find_and_remove(self, arc: Arc):
        if arc == self.arc:
            self._delete_node(self)
        elif arc < self.arc:
            if self.left_node:
                self.left_node.find_and_remove(arc)
            else:
                raise "ValueNotFoundException"
        elif arc > self.arc:
            if self.right_node:
                self.right_node.find_and_remove(arc)
            else:
                raise "ValueNotFoundException"
        else:
            raise "ValueNotFoundException"

    # __init__ as defined
    def _delete_node(self, node: 'BSTNode'):
        """
        This utility function deletes a BSTNode from the BST
        :param node: Must be of type BSTNode
        :return:
        """
        # We delete its children first
        if node.left_node:
            self._delete_node(node.left_node)
        if node.right_node:
            self._delete_node(node.right_node)
        # We remove the pointer of the parent to this node
        parent = node.root_node
        if parent.left_node == node:
            parent.left_node = None
        elif parent.right_node == node:
            parent.right_node = None
        # Finally we delete it
        del node

    def find(self, value: Vertex | Arc) -> 'BSTNode':
        """
        Finds a BSTNode based on a vert or an arc
        :param value: The searching item
        :return: The found BSTNode object
        """
        # TODO (negligible): Implement proper exception handling
        if type(value) == Vertex:
            if value == self.arc.focus:
                return self
            elif value < self.arc.focus:
                if self.left_node:
                    return self.left_node.find(value)
                else:
                    raise "ValueNotFoundException"
            elif value > self.arc.focus:
                if self.right_node:
                    return self.right_node.find(value)
                else:
                    raise "ValueNotFoundException"
            else:
                raise "ValueNotFoundException"
        elif type(value) == Arc:
            if value == self.arc:
                return self
            elif value < self.arc:
                if self.left_node:
                    return self.left_node.find(value)
                else:
                    raise "ValueNotFoundException"
            elif value > self.arc:
                if self.right_node:
                    return self.right_node.find(value)
                else:
                    raise "ValueNotFoundException"
            else:
                raise "ValueNotFoundException"
        else:
            raise "UnsupportedTypeException"

    def search_arc_above_vert(self, vert: Vertex) -> Arc:
        # TODO (negligible): check the pertinence of inequalities (>= <=)
        # This node is above the asked point/focus
        if self.arc.lower_bound() <= vert.x <= self.arc.upper_bound():
            return self.arc
        # This node is on the right of the asked point
        # We redirect the search to the left
        elif vert.x <= self.arc.lower_bound():
            if self.left_node:
                return self.left_node.search_arc_above_vert(vert)
            else:
                raise "ValueNotFoundException"
        # This node is on the left of the asked point
        # We redirect the search to the right
        elif vert.x >= self.arc.upper_bound():
            if self.right_node:
                return self.right_node.search_arc_above_vert(vert)
            else:
                raise "ValueNotFoundException"
