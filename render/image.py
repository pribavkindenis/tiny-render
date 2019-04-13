import numpy as np
from typing import *
from PIL import Image as PILImage


class Image:

    DEFAULT_COLOR = [0, 0, 0, 255]

    def __init__(self, width, height):
        self._matrix = np.empty((height, width, 4)).astype(np.uint8)
        self._matrix[:, :] = self.DEFAULT_COLOR

    def save_image(self, path: str = "image.png"):
        PILImage.fromarray(self._matrix).save(path)

    def __getitem__(self, key: Union[Tuple[Union[int, slice]], Union[int, slice]]):
        return self._matrix[key]

    def __setitem__(self, key: Union[Tuple[Union[int, slice]], Union[int, slice]], value):
        self._matrix[key] = value
