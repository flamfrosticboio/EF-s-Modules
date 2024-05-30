from typing import overload, Sequence
from operator import index as get_index

class Node:
    def __init__(self, value, next = None, index = 0) -> None:
        self.value = value
        self.next = next
        self.index = index

    def __index__(self):
        return int(self.index)
    
    def __int__(self):
        return int(self.value)
    
    def __float__(self):
        return float(self.value)

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
            if i < len(values):
                current.next = Node(values[i], index = i)

        self.do_algorithm(create)

        self._current = self.head
        
    def get_values(self) -> list[int | float]:
        result = []
        for node in self:
            result.append(int(node.value))
        return result

    def __repr__(self) -> str:
        return f"LinkedList({', '.join(map(lambda x:str(x), self.get_values()))})"
    
    def __iter__(self):
        self._current = self.head
        return self
    
    def __next__(self):
        self._current = self._current.next  # type:ignore
        if self._current is None: raise StopIteration
        return self._current

class LinkedList_Extended(LinkedList):
    def __getitem__(self, _index) -> Node:
        _index = get_index(_index)
        for index, node in enumerate(self):
            if index == _index: return node
        raise IndexError("Index out of range.")
    
    def __setitem__(self, _index, value):
        node = self[_index]
        node.value = value

class DataWrapper:
    def __init__(self, values) -> None:
        self.values = values

    def __repr__(self) -> str:
        return f"DataWrapper({repr(self.values)})"

def _has_method(obj, name):
    name = "__" + name + "__"
    return hasattr(obj, name) and callable(getattr(obj, name))

def get_iter_len(obj):
    if _has_method(obj, "len"): return len(obj)
    length = 0
    for _ in obj:
        length += 1
    return length

def _ival(t):
    if _has_method(t, "int"):
        return int(t)
    elif _has_method(t, "float"):
        return float(t)
    return t

def deep_same_list(a, b):
    if _has_method(a, "iter") and _has_method(b, "iter"):
        if get_iter_len(a) != get_iter_len(b):
            print("Length not same!") 
            return False
        return all(deep_same_list(sub1, sub2) for sub1, sub2 in zip(a, b))
    return isinstance(_ival(a), (int, float)) and isinstance(_ival(b), (int, float))

if __name__ == "__main__":
    from pygame import Rect
    print("Final Result:", deep_same_list(Rect(1, 2, 3, 4), ['1', 2, 3, 4]))