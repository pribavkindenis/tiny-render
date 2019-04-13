
class Color:
    def __init__(self, r: int, g: int, b: int, a: int = 255, intensity: float = 1):
        self._intensity = intensity
        self._r = r
        self._g = g
        self._b = b
        self._a = a

    def as_list(self):
        return [
            self._r * self._intensity,
            self._g * self._intensity,
            self._b * self._intensity,
            self._a
        ]

    def set_intensity(self, intensity):
        self._intensity = intensity
