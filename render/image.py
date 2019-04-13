import numpy as np
from typing import *
from PIL import Image as PILImage
from render.color import Color


class Image:

    def __init__(self, width, height, fill_color: Color = Color(0, 0, 0, 255)):
        self._matrix = np.empty((height, width, 4)).astype(np.uint8)
        self._matrix[:, :] = fill_color.as_list()

    def save_image(self, path: str = "image.png"):
        PILImage.fromarray(self._matrix).save(path)

    def __getitem__(self, key: Union[Tuple[Union[int, slice]], Union[int, slice]]):
        return self._matrix[key]

    def __setitem__(self, key: Union[Tuple[Union[int, slice]], Union[int, slice]], color: Color):
        if isinstance(color, Color):
            self._matrix[key] = color.as_list()
        else:
            raise ValueError("Assignable value must be a Color instance")
