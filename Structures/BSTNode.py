from Structures.Arc import Arc
from Structures.Vertex import Vertex


class BSTNode:
    def __init__(self, arc: Arc | None,
                 root_node: 'BSTNode' = None,
                 left_node: 'BSTNode' = None,
                 right_node: 'BSTNode' = None):
        """
        This class implements an x-coordinate sorted BST (left to right
        min to max X)
        :param arc: The arc to assign to this node (if any)
        :param root_node: The parent of this node (if any)
        :param left_node: The left node of this node (if any)
        :param right_node: The right node of this node (if any)
        """
        self.root_node = root_node
        self.left_node = left_node
        self.right_node = right_node
        self.arc = arc

    def inorder(self):
        """
        Utility function to print the BST in-order (min to max X)
        """
        if self is None:
            return
        if self.left_node:
            self.left_node.inorder()
        print(self.arc.focus, end="-")
        if self.right_node:
            self.right_node.inorder()

    def find_and_remove(self, arc: Arc, directrix: float):
        """
        Function able to find a node based on its data and can then delete it
        :param directrix: The value of the directrix
        :param arc: The arc value to delete in this BST
        """
        if arc == self.arc:
            self._delete()
        elif arc.upper_bound(directrix) < self.arc.lower_bound(directrix):
            if self.left_node:
                self.left_node.find_and_remove(arc, directrix)
            else:
                raise "ValueNotFoundException"
        elif arc.lower_bound(directrix) > self.arc.upper_bound(directrix):
            if self.right_node:
                self.right_node.find_and_remove(arc, directrix)
            else:
                raise "ValueNotFoundException"
        else:
            raise "ValueNotFoundException"

    def _delete(self):
        """
        This utility function deletes a BSTNode from the BST
        """
        parent = self.root_node
        # Case 1 : No children, simple case
        if not self.left_node and not self.right_node:
            # First we break the reference
            if parent and parent.right_node == self:
                parent.right_node = None
            elif parent and parent.left_node == self:
                parent.left_node = None
            # Second we delete it
            del self
        # Case 2 : One child that will become the successor
        elif not self.left_node or not self.right_node:
            # If the only child is the left node
            if self.left_node:
                # METHOD 1 : references/pointers update (removal of the node)
                self.left_node.root_node = self.root_node
                if parent and parent.right_node == self:
                    parent.right_node = self.left_node
                elif parent and parent.left_node == self:
                    parent.left_node = self.left_node
                # Then we delete it
                del self
            # If the only child is the right node
            elif self.right_node:
                # METHOD 2 : stealing data + deleting
                self.arc = self.right_node.arc
                self.right_node._delete()
        # Case 3 : Two children
        elif self.right_node and self.left_node:
            # First, find the inorder successor (leftmost node of right subtree)
            successor = self.right_node._find_successor()
            # Secondly, we update data (data replacement instead of updating
            # references/pointers)
            self.arc = successor.arc
            successor._delete()

    def find(self, arc: Arc, directrix: float) -> 'BSTNode':
        """
        Finds a BSTNode based on a vert or an arc
        :param directrix:
        :param arc: The searching item
        :return: The found BSTNode object
        """
        # TODO (negligible): Implement proper exception handling
        if arc == self.arc:
            return self
        elif arc.upper_bound(directrix) < self.arc.lower_bound(directrix):
            if self.left_node:
                return self.left_node.find(arc, directrix)
            else:
                raise "ValueNotFoundException"
        elif arc.lower_bound(directrix) > self.arc.upper_bound(directrix):
            if self.right_node:
                return self.right_node.find(arc, directrix)
            else:
                raise "ValueNotFoundException"
        else:
            raise "ValueNotFoundException"

    def search_arc_above_vert(self, vert: Vertex, directrix: float) -> Arc| None:
        """
        Function to find the arc directly above a vertex
        :param vert: The vertex we want to find the arc above it
        :param directrix: The value of the directrix of all the arcs
        :return: The arc searched if found, otherwise None
        """
        # TODO (negligible): check the pertinence of inequalities (>= <=)
        # What if there are no arcs above?
        if not self.arc:
            return None
        # This node is above the asked point/focus
        if (self.arc.lower_bound(directrix) <= vert.x
                <= self.arc.upper_bound(directrix)):
            return self.arc
        # This node is on the right of the asked point
        # We redirect the search to the left
        elif vert.x <= self.arc.lower_bound(directrix):
            if self.left_node:
                return self.left_node.search_arc_above_vert(vert, directrix)
            else:
                raise "ValueNotFoundException"
        # This node is on the left of the asked point
        # We redirect the search to the right
        elif vert.x >= self.arc.upper_bound(directrix):
            if self.right_node:
                return self.right_node.search_arc_above_vert(vert, directrix)
            else:
                raise "ValueNotFoundException"

    def _find_successor(self) -> 'BSTNode':
        """
        This function recursively finds the left-most node
        :return: The found left-most node
        """
        if self.left_node:
            return self.left_node._find_successor()
        else:
            return self
