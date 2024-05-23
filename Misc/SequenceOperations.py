"""
This module gives operations on sequences. It is recommended to use Vectors.
There are flags you can toggle using set_flag().
In using sequence operations (<operation>S), the creation of sequence sends you a generator expression.
"""

from typing import Any, TypeVar, TypeVarTuple, Tuple, List
from operator import index
from math import floor, ceil

SeqT = TypeVar("SeqT")

# ### Autobuild Script ###
# operations = {'add': "+", "sub": "-", "mul": "*", "div": "/", "fdiv": "//", "pow": "**", "mod": "%",
#               'lshift': "<<", "rshift": ">>", "and": "&", "or": "|", "xor": "^"}
# conversions = {"neg": "-", "abs": ("abs(", ")"), "inv": "~", "toint": ("int(", ")"), 
#                     "tofloat": ("float(", ")"), "toindex": ("index(", ")"), "round": ("round(", ")"),
#                     "floor": ("floor(", ")"), "ceil": ("ceil(", ")")}

# for type in ('tuple', 'list', 'sequence'):
#     for name, operation in operations.items():
#         print(f"def {name}{type[0].upper()}(a: {type.capitalize()}[int | float, ...], b: {type.capitalize()}[int | float, ...]) -> {type.capitalize()}[int | float, ...]:")
#         print(f'    """Equivalent to a {operation} b for every item in a {type}."""')
#         print("    guard_check(a, b)")
#         print(f"    return {type}(x {operation} y for x, y in zip(a, b))")
#         print("")

#     for name, operation in conversions.items():
#         spanned = isinstance(operation, tuple)
#         print(f"def {name}{type[0].upper()}(a: {type.capitalize()}[int | float, ...]) -> {type.capitalize()}[int | float, ...]:")
#         print(f'    """Equivalent to {operation[0] if spanned else operation}a{operation[1] if spanned else ""} for every item in a {type}."""')
#         print(f"    return {type}({operation[0] if spanned else operation}x{operation[1] if spanned else ''} for x in a)")
#         print("")

### ### Main Code ### ###

# Flags
allow_any_length = False
disable_type_check = False

# Exceptions
class LengthError(BaseException): pass

# Built in functions
def set_flag(flag_name: str, toggle: bool):
    flag = globals().get(flag_name)
    if flag: globals().update({flag_name: toggle})

def guard_check(a, b):
    if not allow_any_length and (la:=len(tuple(a))) != (lb:=len(tuple(b))):
        raise LengthError(f"Length of a[{la}] and b[{lb}] not matched.")

# All operations
def addT(a: Tuple[int | float, ...], b: Tuple[int | float, ...]) -> Tuple[int | float, ...]:
    """Equivalent to a + b for every item in a tuple."""
    guard_check(a, b)
    return tuple(x + y for x, y in zip(a, b))

def subT(a: Tuple[int | float, ...], b: Tuple[int | float, ...]) -> Tuple[int | float, ...]:
    """Equivalent to a - b for every item in a tuple."""
    guard_check(a, b)
    return tuple(x - y for x, y in zip(a, b))

def mulT(a: Tuple[int | float, ...], b: Tuple[int | float, ...]) -> Tuple[int | float, ...]:
    """Equivalent to a * b for every item in a tuple."""
    guard_check(a, b)
    return tuple(x * y for x, y in zip(a, b))

def divT(a: Tuple[int | float, ...], b: Tuple[int | float, ...]) -> Tuple[int | float, ...]:
    """Equivalent to a / b for every item in a tuple."""
    guard_check(a, b)
    return tuple(x / y for x, y in zip(a, b))

def fdivT(a: Tuple[int | float, ...], b: Tuple[int | float, ...]) -> Tuple[int | float, ...]:
    """Equivalent to a // b for every item in a tuple."""
    guard_check(a, b)
    return tuple(x // y for x, y in zip(a, b))

def powT(a: Tuple[int | float, ...], b: Tuple[int | float, ...]) -> Tuple[int | float, ...]:
    """Equivalent to a ** b for every item in a tuple."""
    guard_check(a, b)
    return tuple(x ** y for x, y in zip(a, b))

def modT(a: Tuple[int | float, ...], b: Tuple[int | float, ...]) -> Tuple[int | float, ...]:
    """Equivalent to a % b for every item in a tuple."""
    guard_check(a, b)
    return tuple(x % y for x, y in zip(a, b))

def lshiftT(a: Tuple[int | float, ...], b: Tuple[int | float, ...]) -> Tuple[int | float, ...]:
    """Equivalent to a << b for every item in a tuple."""
    guard_check(a, b)
    return tuple(x << y for x, y in zip(a, b))

def rshiftT(a: Tuple[int | float, ...], b: Tuple[int | float, ...]) -> Tuple[int | float, ...]:
    """Equivalent to a >> b for every item in a tuple."""
    guard_check(a, b)
    return tuple(x >> y for x, y in zip(a, b))

def andT(a: Tuple[int | float, ...], b: Tuple[int | float, ...]) -> Tuple[int | float, ...]:
    """Equivalent to a & b for every item in a tuple."""
    guard_check(a, b)
    return tuple(x & y for x, y in zip(a, b))

def orT(a: Tuple[int | float, ...], b: Tuple[int | float, ...]) -> Tuple[int | float, ...]:
    """Equivalent to a | b for every item in a tuple."""
    guard_check(a, b)
    return tuple(x | y for x, y in zip(a, b))

def xorT(a: Tuple[int | float, ...], b: Tuple[int | float, ...]) -> Tuple[int | float, ...]:
    """Equivalent to a ^ b for every item in a tuple."""
    guard_check(a, b)
    return tuple(x ^ y for x, y in zip(a, b))

def negT(a: Tuple[int | float, ...]) -> Tuple[int | float, ...]:
    """Equivalent to -a for every item in a tuple."""
    return tuple(-x for x in a)

def absT(a: Tuple[int | float, ...]) -> Tuple[int | float, ...]:
    """Equivalent to abs(a) for every item in a tuple."""
    return tuple(abs(x) for x in a)

def invT(a: Tuple[int | float, ...]) -> Tuple[int | float, ...]:
    """Equivalent to ~a for every item in a tuple."""
    return tuple(~x for x in a)

def tointT(a: Tuple[int | float, ...]) -> Tuple[int | float, ...]:
    """Equivalent to int(a) for every item in a tuple."""
    return tuple(int(x) for x in a)

def tofloatT(a: Tuple[int | float, ...]) -> Tuple[int | float, ...]:
    """Equivalent to float(a) for every item in a tuple."""
    return tuple(float(x) for x in a)

def toindexT(a: Tuple[int | float, ...]) -> Tuple[int | float, ...]:
    """Equivalent to index(a) for every item in a tuple."""
    return tuple(index(x) for x in a)

def roundT(a: Tuple[int | float, ...]) -> Tuple[int | float, ...]:
    """Equivalent to round(a) for every item in a tuple."""
    return tuple(round(x) for x in a)

def floorT(a: Tuple[int | float, ...]) -> Tuple[int | float, ...]:
    """Equivalent to floor(a) for every item in a tuple."""
    return tuple(floor(x) for x in a)

def ceilT(a: Tuple[int | float, ...]) -> Tuple[int | float, ...]:
    """Equivalent to ceil(a) for every item in a tuple."""
    return tuple(ceil(x) for x in a)

def addL(a: List[int | float], b: List[int | float]) -> List[int | float]:
    """Equivalent to a + b for every item in a list."""
    guard_check(a, b)
    return list(x + y for x, y in zip(a, b))

def subL(a: List[int | float], b: List[int | float]) -> List[int | float]:
    """Equivalent to a - b for every item in a list."""
    guard_check(a, b)
    return list(x - y for x, y in zip(a, b))

def mulL(a: List[int | float], b: List[int | float]) -> List[int | float]:
    """Equivalent to a * b for every item in a list."""
    guard_check(a, b)
    return list(x * y for x, y in zip(a, b))

def divL(a: List[int | float], b: List[int | float]) -> List[int | float]:
    """Equivalent to a / b for every item in a list."""
    guard_check(a, b)
    return list(x / y for x, y in zip(a, b))

def fdivL(a: List[int | float], b: List[int | float]) -> List[int | float]:
    """Equivalent to a // b for every item in a list."""
    guard_check(a, b)
    return list(x // y for x, y in zip(a, b))

def powL(a: List[int | float], b: List[int | float]) -> List[int | float]:
    """Equivalent to a ** b for every item in a list."""
    guard_check(a, b)
    return list(x ** y for x, y in zip(a, b))

def modL(a: List[int | float], b: List[int | float]) -> List[int | float]:
    """Equivalent to a % b for every item in a list."""
    guard_check(a, b)
    return list(x % y for x, y in zip(a, b))

def lshiftL(a: List[int | float], b: List[int | float]) -> List[int | float]:
    """Equivalent to a << b for every item in a list."""
    guard_check(a, b)
    return list(x << y for x, y in zip(a, b))

def rshiftL(a: List[int | float], b: List[int | float]) -> List[int | float]:
    """Equivalent to a >> b for every item in a list."""
    guard_check(a, b)
    return list(x >> y for x, y in zip(a, b))

def andL(a: List[int | float], b: List[int | float]) -> List[int | float]:
    """Equivalent to a & b for every item in a list."""
    guard_check(a, b)
    return list(x & y for x, y in zip(a, b))

def orL(a: List[int | float], b: List[int | float]) -> List[int | float]:
    """Equivalent to a | b for every item in a list."""
    guard_check(a, b)
    return list(x | y for x, y in zip(a, b))

def xorL(a: List[int | float], b: List[int | float]) -> List[int | float]:
    """Equivalent to a ^ b for every item in a list."""
    guard_check(a, b)
    return list(x ^ y for x, y in zip(a, b))

def negL(a: List[int | float]) -> List[int | float]:
    """Equivalent to -a for every item in a list."""
    return list(-x for x in a)

def absL(a: List[int | float]) -> List[int | float]:
    """Equivalent to abs(a) for every item in a list."""
    return list(abs(x) for x in a)

def invL(a: List[int | float]) -> List[int | float]:
    """Equivalent to ~a for every item in a list."""
    return list(~x for x in a)

def tointL(a: List[int | float]) -> List[int | float]:
    """Equivalent to int(a) for every item in a list."""
    return list(int(x) for x in a)

def tofloatL(a: List[int | float]) -> List[int | float]:
    """Equivalent to float(a) for every item in a list."""
    return list(float(x) for x in a)

def toindexL(a: List[int | float]) -> List[int | float]:
    """Equivalent to index(a) for every item in a list."""
    return list(index(x) for x in a)

def roundL(a: List[int | float]) -> List[int | float]:
    """Equivalent to round(a) for every item in a list."""
    return list(round(x) for x in a)

def floorL(a: List[int | float]) -> List[int | float]:
    """Equivalent to floor(a) for every item in a list."""
    return list(floor(x) for x in a)

def ceilL(a: List[int | float]) -> List[int | float]:
    """Equivalent to ceil(a) for every item in a list."""
    return list(ceil(x) for x in a)

def addS(a: SeqT, b: SeqT) -> SeqT:
    """Equivalent to a + b for every item in a sequence. Note: It will create a new class based on parameter 'a' and pass parameters of a generator expression."""
    guard_check(a, b)
    return a.__class__(x + y for x, y in zip(a, b))

def subS(a: SeqT, b: SeqT) -> SeqT:
    """Equivalent to a - b for every item in a sequence. Note: It will create a new class based on parameter 'a' and pass parameters of a generator expression."""
    guard_check(a, b)
    return a.__class__(x - y for x, y in zip(a, b))

def mulS(a: SeqT, b: SeqT) -> SeqT:
    """Equivalent to a * b for every item in a sequence. Note: It will create a new class based on parameter 'a' and pass parameters of a generator expression."""
    guard_check(a, b)
    return a.__class__(x * y for x, y in zip(a, b))

def divS(a: SeqT, b: SeqT) -> SeqT:
    """Equivalent to a / b for every item in a sequence. Note: It will create a new class based on parameter 'a' and pass parameters of a generator expression."""
    guard_check(a, b)
    return a.__class__(x / y for x, y in zip(a, b))

def fdivS(a: SeqT, b: SeqT) -> SeqT:
    """Equivalent to a // b for every item in a sequence. Note: It will create a new class based on parameter 'a' and pass parameters of a generator expression."""
    guard_check(a, b)
    return a.__class__(x // y for x, y in zip(a, b))

def powS(a: SeqT, b: SeqT) -> SeqT:
    """Equivalent to a ** b for every item in a sequence. Note: It will create a new class based on parameter 'a' and pass parameters of a generator expression."""
    guard_check(a, b)
    return a.__class__(x ** y for x, y in zip(a, b))

def modS(a: SeqT, b: SeqT) -> SeqT:
    """Equivalent to a % b for every item in a sequence. Note: It will create a new class based on parameter 'a' and pass parameters of a generator expression."""
    guard_check(a, b)
    return a.__class__(x % y for x, y in zip(a, b))

def lshiftS(a: SeqT, b: SeqT) -> SeqT:
    """Equivalent to a << b for every item in a sequence. Note: It will create a new class based on parameter 'a' and pass parameters of a generator expression."""
    guard_check(a, b)
    return a.__class__(x << y for x, y in zip(a, b))

def rshiftS(a: SeqT, b: SeqT) -> SeqT:
    """Equivalent to a >> b for every item in a sequence. Note: It will create a new class based on parameter 'a' and pass parameters of a generator expression."""
    guard_check(a, b)
    return a.__class__(x >> y for x, y in zip(a, b))

def andS(a: SeqT, b: SeqT) -> SeqT:
    """Equivalent to a & b for every item in a sequence. Note: It will create a new class based on parameter 'a' and pass parameters of a generator expression."""
    guard_check(a, b)
    return a.__class__(x & y for x, y in zip(a, b))

def orS(a: SeqT, b: SeqT) -> SeqT:
    """Equivalent to a | b for every item in a sequence. Note: It will create a new class based on parameter 'a' and pass parameters of a generator expression."""
    guard_check(a, b)
    return a.__class__(x | y for x, y in zip(a, b))

def xorS(a: SeqT, b: SeqT) -> SeqT:
    """Equivalent to a ^ b for every item in a sequence. Note: It will create a new class based on parameter 'a' and pass parameters of a generator expression."""
    guard_check(a, b)
    return a.__class__(x ^ y for x, y in zip(a, b))

def negS(a: SeqT) -> SeqT:
    """Equivalent to -a for every item in a sequence. Note: It will create a new class based on parameter 'a' and pass parameters of a generator expression."""
    return a.__class__(-x for x in a)

def absS(a: SeqT) -> SeqT:
    """Equivalent to abs(a) for every item in a sequence. Note: It will create a new class based on parameter 'a' and pass parameters of a generator expression."""
    return a.__class__(abs(x) for x in a)

def invS(a: SeqT) -> SeqT:
    """Equivalent to ~a for every item in a sequence. Note: It will create a new class based on parameter 'a' and pass parameters of a generator expression."""
    return a.__class__(~x for x in a)

def tointS(a: SeqT) -> SeqT:
    """Equivalent to int(a) for every item in a sequence. Note: It will create a new class based on parameter 'a' and pass parameters of a generator expression."""
    return a.__class__(int(x) for x in a)

def tofloatS(a: SeqT) -> SeqT:
    """Equivalent to float(a) for every item in a sequence. Note: It will create a new class based on parameter 'a' and pass parameters of a generator expression."""
    return a.__class__(float(x) for x in a)

def toindexS(a: SeqT) -> SeqT:
    """Equivalent to index(a) for every item in a sequence. Note: It will create a new class based on parameter 'a' and pass parameters of a generator expression."""
    return a.__class__(index(x) for x in a)

def roundS(a: SeqT) -> SeqT:
    """Equivalent to round(a) for every item in a sequence. Note: It will create a new class based on parameter 'a' and pass parameters of a generator expression."""
    return a.__class__(round(x) for x in a)

def floorS(a: SeqT) -> SeqT:
    """Equivalent to floor(a) for every item in a sequence. Note: It will create a new class based on parameter 'a' and pass parameters of a generator expression."""
    return a.__class__(floor(x) for x in a)

def ceilS(a: SeqT) -> SeqT:
    """Equivalent to ceil(a) for every item in a sequence. Note: It will create a new class based on parameter 'a' and pass parameters of a generator expression."""
    return a.__class__(ceil(x) for x in a)