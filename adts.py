import heapq

class Stack:
    def __init__(self, item=None):
        if item is not None:
            self._contents = [item]
        self._contents = []

    def is_empty(self):
        return len(self._contents) == 0

    def add(self, item):
        self._contents += [item]

    def add_lst(self, lst):
        for item in lst:
            self.add(item)

    def pop(self):
        return self._contents.pop(-1)
