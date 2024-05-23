"""This module is an dictionary of sequence operations in Misc.
Note that this does not rely on SequenceOperations.py

Allowed:
- {key: int | float}
- {key: Sequence[int | float]}
- {key: {key2: {key3: ...}, key4: Sequnce[int | float]}, key5: int | float}  # nested dictionary

The keys for values to be applied is based on the keys exist in parameter 'b'.
"""

from typing import Any, Sequence, Dict, Union, Type

typeof = lambda cls, *args: isinstance(cls, args)   # better isinstance version
classN = lambda cls: cls.__class__.__name__
has_method = lambda cls, name: hasattr(cls, name) and callable(getattr(cls, name))

NestedDict = Dict[Any, Union[int, float, Sequence[Union[int, float]], Dict[Any, 'NestedDict']]]

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