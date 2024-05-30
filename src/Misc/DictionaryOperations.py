"""This module is an dictionary of sequence operations in Misc.
Note that this does not rely on SequenceOperations.py

Allowed:
- {key: int | float}
- {key: Sequence[int | float]}
- {key: {key2: {key3: ...}, key4: Sequnce[int | float]}, key5: int | float}  # nested dictionary

The keys for values to be applied is based on the keys exist in parameter 'b'.
"""

from typing import Any, Sequence, Dict, Union
from math import floor, ceil
from operator import index

typeof = lambda cls, *args: isinstance(cls, args)   # better isinstance version
classN = lambda cls: cls.__class__.__name__
has_method = lambda cls, name: hasattr(cls, name) and callable(getattr(cls, name))

NestedDict = Dict[Any, Union[int, float, Any, Sequence[Union[int, float, Any]], Dict[Any, 'NestedDict']]]

# ### AutoScript ###
# operations = {'add': "+", "sub": "-", "mul": "*", "div": "/", "fdiv": "//", "pow": "**", "mod": "%",
#               'lshift': "<<", "rshift": ">>", "and": "&", "or": "|", "xor": "^"}
# conversions = {"neg": "-", "abs": ("abs(", ")"), "inv": "~", "toint": ("int(", ")"), 
#                     "tofloat": ("float(", ")"), "toindex": ("index(", ")"), "round": ("round(", ")"),
#                     "floor": ("floor(", ")"), "ceil": ("ceil(", ")")}
# for name, operation in operations.items():
#     print(f"def {name}D(a: NestedDict, b: NestedDict) -> NestedDict:")
#     print(f'    """Equivalent to a {operation} b for every key in a dict or sequence in a dict."""')
#     print(f"    return _deep_apply(a, b, lambda x, y: x {operation} y)")
#     print("")

# for name, operation in conversions.items():
#     spanned = isinstance(operation, tuple)
#     print(f"def {name}D(a: NestedDict) -> NestedDict:")
#     print(f'    """Equivalent to {operation[0] if spanned else operation}a{operation[1] if spanned else ""} for every item in a dictionary."""')
#     print(f"    return _deep_convert(a, lambda x: {operation[0] if spanned else operation}x{operation[1] if spanned else ''})")
#     print("")

def _deep_apply(a, b, f):
    result = {}
    for key in b:
        if typeof(a[key], int, float):
            if typeof(b[key], int, float):
                result[key] = f(a[key], b[key])
            else:
                raise TypeError(f"Types don't match for {classN(a)} and {classN(b)}")
        elif has_method(b[key], "__iter__"):
            if typeof(a[key], dict): 
                if typeof(b[key], dict):
                    result[key] = _deep_apply(a[key], b[key], f)
                else:
                    raise TypeError(f"Types don't match for {classN(a)} and {classN(b)}")
            else:
                result[key] = a[key].__class__(f(a[key][i], b[key][i]) for i, _ in enumerate(b[key]))
        else:
            raise TypeError(f"Types don't match for {classN(a)} and {classN(b)}")
    return result

def _deep_convert(a, f):
    result = {}
    for key in a:
        if typeof(a[key], int, float):
            result[key] = f(a[key])
        elif typeof(a[key], dict):
            result[key] = _deep_convert(a[key], f)
        elif has_method(a[key], "__iter__"):
            result[key] = a[key].__class__(f(a[key][i]) for i, _ in enumerate(a[key]))
        else:
            raise TypeError(f"Unsupported Type: {classN(a)}")
    return result

def addD(a: NestedDict, b: NestedDict) -> NestedDict:
    """Equivalent to a + b for every key in a dict or sequence in a dict."""
    return _deep_apply(a, b, lambda x, y: x + y)

def subD(a: NestedDict, b: NestedDict) -> NestedDict:
    """Equivalent to a - b for every key in a dict or sequence in a dict."""
    return _deep_apply(a, b, lambda x, y: x - y)

def mulD(a: NestedDict, b: NestedDict) -> NestedDict:
    """Equivalent to a * b for every key in a dict or sequence in a dict."""
    return _deep_apply(a, b, lambda x, y: x * y)

def divD(a: NestedDict, b: NestedDict) -> NestedDict:
    """Equivalent to a / b for every key in a dict or sequence in a dict."""
    return _deep_apply(a, b, lambda x, y: x / y)

def fdivD(a: NestedDict, b: NestedDict) -> NestedDict:
    """Equivalent to a // b for every key in a dict or sequence in a dict."""
    return _deep_apply(a, b, lambda x, y: x // y)

def powD(a: NestedDict, b: NestedDict) -> NestedDict:
    """Equivalent to a ** b for every key in a dict or sequence in a dict."""
    return _deep_apply(a, b, lambda x, y: x ** y)

def modD(a: NestedDict, b: NestedDict) -> NestedDict:
    """Equivalent to a % b for every key in a dict or sequence in a dict."""
    return _deep_apply(a, b, lambda x, y: x % y)

def lshiftD(a: NestedDict, b: NestedDict) -> NestedDict:
    """Equivalent to a << b for every key in a dict or sequence in a dict."""
    return _deep_apply(a, b, lambda x, y: x << y)

def rshiftD(a: NestedDict, b: NestedDict) -> NestedDict:
    """Equivalent to a >> b for every key in a dict or sequence in a dict."""
    return _deep_apply(a, b, lambda x, y: x >> y)

def andD(a: NestedDict, b: NestedDict) -> NestedDict:
    """Equivalent to a & b for every key in a dict or sequence in a dict."""
    return _deep_apply(a, b, lambda x, y: x & y)

def orD(a: NestedDict, b: NestedDict) -> NestedDict:
    """Equivalent to a | b for every key in a dict or sequence in a dict."""
    return _deep_apply(a, b, lambda x, y: x | y)

def xorD(a: NestedDict, b: NestedDict) -> NestedDict:
    """Equivalent to a ^ b for every key in a dict or sequence in a dict."""
    return _deep_apply(a, b, lambda x, y: x ^ y)

def negD(a: NestedDict) -> NestedDict:
    """Equivalent to -a for every item in a dictionary."""
    return _deep_convert(a, lambda x: -x)

def absD(a: NestedDict) -> NestedDict:
    """Equivalent to abs(a) for every item in a dictionary."""
    return _deep_convert(a, lambda x: abs(x))

def invD(a: NestedDict) -> NestedDict:
    """Equivalent to ~a for every item in a dictionary."""
    return _deep_convert(a, lambda x: ~x)

def tointD(a: NestedDict) -> NestedDict:
    """Equivalent to int(a) for every item in a dictionary."""
    return _deep_convert(a, lambda x: int(x))

def tofloatD(a: NestedDict) -> NestedDict:
    """Equivalent to float(a) for every item in a dictionary."""
    return _deep_convert(a, lambda x: float(x))

def toindexD(a: NestedDict) -> NestedDict:
    """Equivalent to index(a) for every item in a dictionary."""
    return _deep_convert(a, lambda x: index(x))

def roundD(a: NestedDict) -> NestedDict:
    """Equivalent to round(a) for every item in a dictionary."""
    return _deep_convert(a, lambda x: round(x))

def floorD(a: NestedDict) -> NestedDict:
    """Equivalent to floor(a) for every item in a dictionary."""
    return _deep_convert(a, lambda x: floor(x))

def ceilD(a: NestedDict) -> NestedDict:
    """Equivalent to ceil(a) for every item in a dictionary."""
    return _deep_convert(a, lambda x: ceil(x))