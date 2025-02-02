from samson.math.polynomial import Polynomial

class Infinity(object):
    def __repr__(self):
        return '∞'

    def __eq__(self, other):
        return type(self) == type(other)

    def __str__(self):
        return self.__repr__()

    def __lt__(self, other):
        return False

    def __gt__(self, other):
        return self != other

    def __neg__(self):
        return NegativeInfinity()

    def __add__(self, other):
        if type(other) is NegativeInfinity:
            raise ValueError("Cannot subtract infinity from infinity.")

        return self
    

    def __radd__(self, other):
        return self + other


    def __sub__(self, other):
        if type(other) is Infinity:
            raise ValueError("Cannot subtract infinity from infinity.")

        return self


    def __rsub__(self, other):
        return -self + other


    def __mul__(self, other):
        if not other:
            return other
        elif other == -self:
            return -oo
        
        elif other == self:
            return oo

        return self


    def __rmul__(self, other):
        return self*other

    def __pow__(self, other):
        return self

    def __truediv__(self, other):
        if issubclass(type(other), Infinity):
            raise ValueError("Cannot divide infinity by infinity.")

        return self

    def __rtruediv__(self, other):
        return 0


    def __floordiv__(self, other):
        return self / other


    def __rfloordiv__(self, other):
        return 0


class NegativeInfinity(Infinity):
    def __repr__(self):
        return '-∞'

    def __str__(self):
        return self.__repr__()

    def __lt__(self, other):
        return self != other

    def __gt__(self, other):
        return False

    def __neg__(self):
        return Infinity()


    def __add__(self, other):
        if type(other) is Infinity:
            raise ValueError("Cannot subtract infinity from infinity.")

        return self

    def __sub__(self, other):
        if type(other) is NegativeInfinity:
            raise ValueError("Cannot subtract infinity from infinity.")

        return self


class Symbol(Polynomial):
    def __init__(self, str_representation):
        self.repr = str_representation
        self.ring = None
        self.var  = None
        self.top_ring = None


    def __repr__(self):
        return f'<Symbol: {self.repr}, ring={self.ring}>'

    def __str__(self):
        return self.repr

    def __hash__(self):
        return hash(self.var)

    def __eq__(self, other: 'Symbol') -> bool:
        return type(self) == type(other) and self.repr == other.repr and self.ring == other.ring

    def __bool__(self) -> bool:
        return True


    def __top_coerce(self, poly):
        if self.top_ring:
            poly = self.top_ring(poly)
        return poly


    def __add__(self, other):
        return self.__top_coerce(self.var) + other


    def __sub__(self, other):
        return self.__top_coerce(self.var) - other


    def __mul__(self, other):
        return self.__top_coerce(self.var) * other


    def __invert__(self):
        return ~self.__top_coerce(self.var)


    def __truediv__(self, other):
        return self.__top_coerce(self.var) / other


    def __lshift__(self, other):
        return self.__top_coerce(super().__lshift__(other))


    def __rshift__(self, other):
        return self.__top_coerce(super().__rshift__(other))


    def __divmod__(self, other):
        return divmod(self.__top_coerce(self.var), other)


    def __floordiv__(self, other):
        return self.__top_coerce(self.var) // other


    def __mod__(self, other):
        return self.__top_coerce(self.var) % other


    def __pow__(self, power):
        poly = self.var._create_poly({power: self.ring.ring.one})
        return self.__top_coerce(poly)


    def build(self, ring):
        self.ring = ring
        self.var  = Polynomial([ring.ring.zero, ring.ring.one], coeff_ring=ring.ring, ring=ring, symbol=self)


    def __getattribute__(self, name):
        try:
            attr = object.__getattribute__(self, name)
        except AttributeError:
            attr = object.__getattribute__(self.var, name)

        return attr



oo = Infinity()
