from math import floor, ceil

def deep_equal(a, b):
    for ia, ib in zip(a, b):
        if hasattr(ia, "__iter__"):
            if hasattr(ib, "__iter__"):
                return deep_equal(ia, ib)
            else:
                return False
        elif hasattr(ib, "__iter__"):
            return False
    return len(tuple(a)) == len(tuple(b))
    

class NumericalSequence:
    def __init__(self, *values) -> None:
        if values == ():
            self._val = list()
        elif len(values) > 1:
            self._val = list(values)
        else:
            self._val = list(values[0]) # type: ignore

    def new(self, *values):
        return self.__class__(*values)
    
    def apply(self, other, func):
        for i, a in enumerate(self._val): self._val[i] = func(a, other[i])

    def convert(self, func):
        for i, a in enumerate(self._val): self._val[i] = func(a)

    def convert_int(self): self.convert(lambda x: int(x)); return self
    def convert_float(self): self.convert(lambda x: float(x)); return self
    def convert_complex(self): self.convert(lambda x: complex(x)); return self

    def get_values(self, _return_as = list): return _return_as(self._val)

    def __repr__(self) -> str: return f"{self.__class__.__name__}({self._val})"
    def __hash__(self): return hash(self._val)
    def __bool__(self): return bool(self._val)
    def __len__(self): return len(self._val)
    def __getitem__(self, key): return self._val[key]
    def __setitem__(self, key, value): self._val[key] = value
    def __delitem__(self, key): del self._val[key]
    def __iter__(self): return iter(self._val)
    def __contains__(self, item): return item in self._val

    def __add__(self, other): return self.new(a + b for a, b in zip(self._val, other))
    def __sub__(self, other): return self.new(a - b for a, b in zip(self._val, other))
    def __mul__(self, other): return self.new(a * b for a, b in zip(self._val, other))
    def __truediv__(self, other): return self.new(a / b for a, b in zip(self._val, other))
    def __floordiv__(self, other): return self.new(a // b for a, b in zip(self._val, other))
    def __mod__(self, other): return self.new(a % b for a, b in zip(self._val, other))
    def __pow__(self, other): return self.new(a ** b for a, b in zip(self._val, other))

    def __radd__(self, other): return self.new(b + a for a, b, in zip(self._val, other))
    def __rsub__(self, other): return self.new(b - a for a, b, in zip(self._val, other))
    def __rmul__(self, other): return self.new(b * a for a, b, in zip(self._val, other))
    def __rtruediv__(self, other): return self.new(b / a for a, b, in zip(self._val, other))
    def __rfloordiv__(self, other): return self.new(b // a for a, b, in zip(self._val, other))
    def __rmod__(self, other): return self.new(b % a for a, b, in zip(self._val, other))
    def __rpow__(self, other): return self.new(b ** a for a, b, in zip(self._val, other))

    def __iadd__(self, other): self.apply(other, lambda a, b: a + b); return self
    def __isub__(self, other): self.apply(other, lambda a, b: a - b); return self
    def __imul__(self, other): self.apply(other, lambda a, b: a * b); return self
    def __itruediv__(self, other): self.apply(other, lambda a, b: a / b); return self
    def __ifloordiv__(self, other): self.apply(other, lambda a, b: a // b); return self
    def __imod__(self, other): self.apply(other, lambda a, b: a % b); return self
    def __ipow__(self, other): self.apply(other, lambda a, b: a ** b); return self

    def __neg__(self): self.convert(lambda x: -x); return self
    def __abs__(self): self.convert(lambda x: abs(x)); return self
    def __floor__(self): self.convert(lambda x: floor(x)); return self
    def __ceil__(self): self.convert(lambda x: ceil(x)); return self

class IntSequence(NumericalSequence):
    def convert_bytes(self): self.convert(lambda x: x.to_bytes()); return self

    def __lshift__(self, other): return self.new(a << b for a, b in zip(self._val, other))
    def __rshift__(self, other): return self.new(a >> b for a, b in zip(self._val, other))
    def __and__(self, other): return self.new(a & b for a, b in zip(self._val, other))
    def __xor__(self, other): return self.new(a ^ b for a, b in zip(self._val, other))
    def __or__(self, other): return self.new(a | b for a, b in zip(self._val, other))

    def __rlshift__(self, other): return self.new(b << a for a, b in zip(self._val, other))
    def __rrshift__(self, other): return self.new(b >> a for a, b in zip(self._val, other))
    def __rand__(self, other): return self.new(b & a for a, b in zip(self._val, other))
    def __rxor__(self, other): return self.new(b ^ a for a, b in zip(self._val, other))
    def __ror__(self, other): return self.new(b | a for a, b in zip(self._val, other))

    def __ilshift__(self, other): self.apply(other, lambda a, b: a << b); return self
    def __irshift__(self, other): self.apply(other, lambda a, b: a >> b); return self
    def __iand__(self, other): self.apply(other, lambda a, b: a & b); return self
    def __ixor__(self, other): self.apply(other, lambda a, b: a ^ b); return self
    def __ior__(self, other): self.apply(other, lambda a, b: a | b); return self
    def __invert__(self): self.convert(lambda a: ~a); return self