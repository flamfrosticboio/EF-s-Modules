from typing import overload, Iterable, Self, Callable, Iterator, Union, Any, TypeVar, SupportsIndex

Number = int | float | complex
NumberIterable = Iterable[Number]

_Iterable = Union[Iterable[Any], Iterable['_Iterable']]
_T = TypeVar("_T")

def deep_equal(a: _Iterable, b: _Iterable) -> bool: ...

class NumericalSequence:
    """Creates a numerical sequence with built in operators."""
    @overload
    def __init__(self, values: NumberIterable) -> None: ...

    @overload
    def __init__(self, *values: Number) -> None: ...

    @overload
    def __init__(self) -> None: ...

    def new(self, *values: tuple) -> Self: 
        """Create a new self. Equivalent to self.__init__()"""

    def apply(self, other: NumberIterable, func: Callable[[Number, Number], Number]) -> None:
        """Applies self and other using the function provided. \n- Example: apply([1, 2, 3], lambda a, b: a + b)"""

    def convert(self, func: Callable[[Number], Number]):
        """Converts all values using the function. \n- Example: convert([1, 2, 3], lambda a: -a)"""

    def convert_int(self) -> Self:
        """Converts all values into integers (int)"""

    def convert_float(self) -> Self: 
        """Converts all values into floats (float)"""

    def convert_complex(self) -> Self:
        """Converts all values into complex numbers (complex)"""

    def get_values(self, _return_as: type[_T] = list) -> _T: 
        """Returns all values of this sequence."""

    def __repr__(self) -> str: ...
    def __hash__(self) -> int: ...
    def __bool__(self) -> bool: ...
    def __len__(self) -> int: ...
    def __getitem__(self, key: SupportsIndex) -> Number: ...
    def __setitem__(self, key: SupportsIndex, value: Number) -> None: ...
    def __delitem__(self, key: SupportsIndex) -> None: ...
    def __iter__(self) -> Iterator: ...
    def __contains__(self, item: Any) -> bool: ...

    def __add__(self, other: NumberIterable) -> Self: ...
    def __sub__(self, other: NumberIterable) -> Self: ...
    def __mul__(self, other: NumberIterable) -> Self: ...
    def __truediv__(self, other: NumberIterable) -> Self: ...
    def __floordiv__(self, other: NumberIterable) -> Self: ...
    def __mod__(self, other: NumberIterable) -> Self: ...
    def __pow__(self, other: NumberIterable) -> Self: ...

    def __radd__(self, other: NumberIterable) -> Self: ...
    def __rsub__(self, other: NumberIterable) -> Self: ...
    def __rmul__(self, other: NumberIterable) -> Self: ...
    def __rtruediv__(self, other: NumberIterable) -> Self: ...
    def __rfloordiv__(self, other: NumberIterable) -> Self: ...
    def __rmod__(self, other: NumberIterable) -> Self: ...
    def __rpow__(self, other: NumberIterable) -> Self: ...

    def __iadd__(self, other: NumberIterable) -> Self: ...
    def __isub__(self, other: NumberIterable) -> Self: ...
    def __imul__(self, other: NumberIterable) -> Self: ...
    def __itruediv__(self, other: NumberIterable) -> Self: ...
    def __ifloordiv__(self, other: NumberIterable) -> Self: ...
    def __imod__(self, other: NumberIterable) -> Self: ...
    def __ipow__(self, other: NumberIterable) -> Self: ...

    def __neg__(self) -> Self: ...
    def __abs__(self) -> Self: ...
    def __floor__(self) -> Self: ...
    def __ceil__(self) -> Self: ...

class IntSequence(NumericalSequence):
    """Extended version of NumericalSequence but limited for ints due to int-only operations."""
    
    @overload
    def __init__(self, values: Iterable[int]) -> None: ...

    @overload
    def __init__(self, *values: int) -> None: ...

    @overload
    def __init__(self) -> None: ...

    def convert_bytes(self) -> Self:
        """Converts all values into bytes."""

    def __lshift__(self, other: Iterable[int]) -> Self: ...
    def __rshift__(self, other: Iterable[int]) -> Self: ...
    def __and__(self, other: Iterable[int]) -> Self: ...
    def __xor__(self, other: Iterable[int]) -> Self: ...
    def __or__(self, other: Iterable[int]) -> Self: ...

    def __rlshift__(self, other: Iterable[int]) -> Self: ...
    def __rrshift__(self, other: Iterable[int]) -> Self: ...
    def __rand__(self, other: Iterable[int]) -> Self: ...
    def __rxor__(self, other: Iterable[int]) -> Self: ...
    def __ror__(self, other: Iterable[int]) -> Self: ...

    def __ilshift__(self, other: Iterable[int]) -> Self: ...
    def __irshift__(self, other: Iterable[int]) -> Self: ...
    def __iand__(self, other: Iterable[int]) -> Self: ...
    def __ixor__(self, other: Iterable[int]) -> Self: ...
    def __ior__(self, other: Iterable[int]) -> Self: ...
    def __invert__(self) -> Self: ...