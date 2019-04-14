import numpy as np
from typing import *
from PIL import Image as PILImage
from render.color import Color

KeyType = Union[
    Tuple[int, int],
    Tuple[int, slice],
    Tuple[slice, int],
    Tuple[slice, slice]
]


class Image:

    def __init__(self,
                 width: int,
                 height: int,
                 depth: int = 255,
                 fill_color: Color = Color(0, 0, 0, 255)):
        self._width = width
        self._height = height
        self._depth = depth
        self._matrix = np.empty((height, width, 4)).astype(np.uint8)
        self._matrix[:, :] = fill_color.as_list()

    def save_image(self, path: str = "image.png"):
        PILImage.fromarray(self._matrix[::-1]).save(path)

    def width(self):
        return self._width

    def height(self):
        return self._height

    def depth(self):
        return self._depth

    def __getitem__(self, key: KeyType):
        return self._matrix[key[::-1]]

    def __setitem__(self, key: KeyType, color: Color):
        if isinstance(color, Color):
            self._matrix[key[::-1]] = color.as_list()
        else:
            raise ValueError("Assignable value must be a Color instance")
