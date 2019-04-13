
class Color:
    def __init__(self, r: int, g: int, b: int, a: int):
        self._r = r
        self._g = g
        self._b = b
        self._a = a

    def as_list(self):
        return [self._r, self._g, self._b, self._a]
