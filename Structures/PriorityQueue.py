from Vertex import Vertex
from PointEvent import PointEvent
from Event import Event

class PriorityQueue:
    #TODO: Rework for a faster implementation (Heap)
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