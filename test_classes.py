from typing import overload, Sequence

class Node:
    def __init__(self, value, next = None) -> None:
        self.value = value
        self.next = next

        # TweenService value support
        self.__tw_use_value__ = "value"

    def __repr__(self) -> str:
        return f"Node({self.value})"
    
class LinkedList:
    @overload
    def __init__(self, values: list[int | float] | tuple[int | float, ...] | Sequence[int | float]) -> None: ...

    @overload
    def __init__(self, *list: int | float) -> None: ...

    def do_algorithm(self, func, i = -1):
        current = self.head
        while current is not None:
            i+=1
            func(i, current, locals())
            current = current.next

    def __init__(self, *val):
        values = val[0] if isinstance(val[0], Sequence) else val
        self.head = Node(values[0])

        def create(i, current, locals):
            if i < len(values): current.next = Node(values[i])

        self.do_algorithm(create)

        self._current = self.head
        
    def get_values(self) -> list[int | float]:
        result = []
        self.do_algorithm(lambda a, current, c: result.append(current.value))
        return result[:-1]

    def __repr__(self) -> str:
        return f"LinkedList({', '.join(map(lambda x:str(x), self.get_values()))})"
    
    def __iter__(self):
        self._current = self.head
        return self
    
    def __next__(self):
        self._current = self._current.next
        if self._current is None: raise StopIteration
        return self._current
    
class LinkedList_Extended(LinkedList):
    def __getitem__(self, _index):
        for index, node in enumerate(self):
            if index == _index:
                return node
        raise IndexError("Index out of range.")