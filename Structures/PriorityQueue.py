from Vertex import Vertex
from PointEvent import PointEvent
from Event import Event
from Arc import Arc


class PriorityQueue:
    # TODO: Rework for a faster implementation (Heap / BST)
    # This priority queue is y-sorted (axis of progression of the sweep-line
    def __init__(self, entry: list[Vertex], sorting_func):
        self._value = [PointEvent(x) for x in entry].sort(key=sorting_func)
        self.sorting_func = sorting_func

    def pop_max(self) -> Event:
        if self._value[0]:
            return self._value.pop(0)

    def is_empty(self):
        if len(self._value) != 0:
            return False
        else:
            return True

    def remove(self, event: Event):
        """
        UNTESTED
        To get to know complexity -> read python docs
        :param event:
        :return:
        """
        self._value.remove(event)

    def insert(self, event: Event):
        """
        DOES NOT WORK -> KNOWN
        :param event:
        :return:
        """
        # TODO
        self._value.append(event)
