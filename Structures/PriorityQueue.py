from Structures.PointEvent import PointEvent
from Structures.CircleEvent import CircleEvent

class CustomNode:
    def __init__(self, event: PointEvent | CircleEvent,
                 root_node: 'CustomNode' = None,
                 left_node: 'CustomNode' = None,
                 right_node: 'CustomNode' = None):
        """
        This class implements an Y-coordinate sorted BST (top to bottom
        min to max Y)
        :param event: The event to assign to this node (if any)
        :param root_node: The parent of this node (if any)
        :param left_node: The left node of this node (if any)
        :param right_node: The right node of this node (if any)
        """
        self.root_node = root_node
        self.left_node = left_node
        self.right_node = right_node
        self.events = [event]

    def inorder(self):
        """
        Utility function to print the BST in-order (top to bottom Y)
        """
        if self is None:
            return
        if self.left_node:
            self.left_node.inorder()
        for event in self.events:
            print(event, end="-")
        if self.right_node:
            self.right_node.inorder()

    def insert(self, event: PointEvent | CircleEvent):
        if self.events is None or len(self.events) == 0:
            self.events = [event]
            pass

        if event in self.events:
            raise "NotImplementedException"
        elif event.value < self.events[0].value:
            if not self.left_node:
                self.left_node = CustomNode(event, root_node=self)
            else:
                self.left_node.insert(event)
        elif event.value > self.events[0].value:
            if not self.right_node:
                self.right_node = CustomNode(event, root_node=self)
            else:
                self.right_node.insert(event)
        else:
            raise "NotImplementedException"

    def find_and_remove(self, event: PointEvent | CircleEvent):
        """
        Function able to find a node based on its data and can then delete it
        :param event: The event value to delete in this BST
        """
        if self.events is None or len(self.events) == 0:
            raise "ValueNotFoundException"

        if event in self.events:
            # If there's more than 1 event at this position
            if len(self.events) > 1:
                self.events.remove(event)
            # If this is the only event associated with this node
            else:
                self.delete()
        elif event.value < self.events[0].value:
            if self.left_node:
                self.left_node.find_and_remove(event)
            else:
                raise "ValueNotFoundException"
        elif event.value > self.events[0].value:
            if self.right_node:
                self.right_node.find_and_remove(event)
            else:
                raise "ValueNotFoundException"
        else:
            raise "ValueNotFoundException"

    def delete(self):
        """
        This utility function deletes a CustomNode from the BST
        """
        parent = self.root_node
        # Case 1 : No children, simple case
        if not self.left_node and not self.right_node:
            # First we break the reference
            if parent and parent.right_node == self:
                parent.right_node = None
            elif parent and parent.left_node == self:
                parent.left_node = None
            else:
                # Case where we try to delete the last node (root)
                self.events = None
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
                self.events = self.right_node.events
                self.right_node.delete()
        # Case 3 : Two children
        elif self.right_node and self.left_node:
            # First, find the inorder successor (leftmost node of right subtree)
            successor = self.right_node._find_successor()
            # Secondly, we update data (data replacement instead of updating
            # references/pointers)
            self.events = successor.events
            successor.delete()

    def _find_successor(self) -> 'CustomNode':
        """
        This function recursively finds the left-most node
        :return: The found left-most node
        """
        if self.left_node:
            return self.left_node._find_successor()
        else:
            return self

    def find(self, event: PointEvent | CircleEvent) -> 'CustomNode':
        """
        Finds a CustomNode based on an Event
        :param event: The searching object
        :return: The found BSTNode object
        """
        # TODO (negligible): Implement proper exception handling
        if self.events is None or len(self.events) == 0:
            raise "ValueNotFoundException"

        if event in self.events:
            return self
        elif event.value < self.events[0].value:
            if self.left_node:
                return self.left_node.find(event)
            else:
                raise "ValueNotFoundException"
        elif event.value > self.events[0].value:
            if self.right_node:
                return self.right_node.find(event)
            else:
                raise "ValueNotFoundException"
        else:
            raise "ValueNotFoundException"

    def get_min(self) -> 'CustomNode':
        if self.left_node is not None and len(self.left_node.events) > 0:
            return self.left_node.get_min()
        elif self.left_node is None:
            return self
        else:
            raise "EmptyCustomNodeException"

    def get_max(self) -> 'CustomNode':
        if self.right_node is not None and len(self.right_node.events) > 0:
            return self.right_node.get_min()
        elif self.right_node is None:
            return self
        else:
            raise "EmptyCustomNodeException"


class PriorityQueue:
    def __init__(self, events: list[PointEvent | CircleEvent]):
        self.size = 0
        self.root = CustomNode(events[len(events) // 2])
        for event in events:
            if event != events[len(events) // 2]:
                self.root.insert(event)

    def insert(self, event):
        self.root.insert(event)

    def delete(self, event):
        self.root.find_and_remove(event)

    @property
    def is_empty(self) -> bool:
        if (self.root is None or
                ((self.root.events is None or len(self.root.events) == 0) and
                 self.root.left_node is None and
                 self.root.right_node is None)):
            return True
        else:
            return False

    def pop_min(self) -> list[PointEvent | CircleEvent]:
        node = self.root.get_min()
        events = node.events.copy()
        node.delete()
        return events

    def pop_max(self) -> list[PointEvent | CircleEvent]:
        node = self.root.get_max()
        events = node.events.copy()
        node.delete()
        return events
