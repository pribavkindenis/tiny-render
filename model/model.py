from typing import *
from PIL import Image as PILImage
import numpy as np
import re


class Model:

    @staticmethod
    def parse_obj(path) -> Tuple[List, List, List, List]:
        vn = []
        vt = []
        v = []
        f = []
        with open(path, "r") as file:
            for line in file:
                if line.startswith("vt"):
                    Model.parse_line(line, vt)
                elif line.startswith("vn"):
                    Model.parse_line(line, vn)
                elif line.startswith("v"):
                    Model.parse_line(line, v)
                elif line.startswith("f"):
                    Model.parse_polygon(line, f)
        return vn, vt, v, f

    @staticmethod
    def parse_line(line: str, array: list):
        data = re.split("\\s+", line.strip())
        result = []
        for i in range(1, len(data)):
            try:
                result.append(float(data[i]))
            except ValueError:
                raise IOError("Object file is invalid")
        array.append(result)

    @staticmethod
    def parse_polygon(line: str, array: list):
        data = re.split("\\s+", line.strip())
        result = []
        for i in range(1, len(data)):
            sub_data = data[i].split("/")
            try:
                result.append([
                    int(sub_data[0]) - 1,
                    int(sub_data[1]) - 1,
                    int(sub_data[2]) - 1
                ])
            except ValueError:
                raise IOError("Object file is invalid")
        array.append(result)

    @staticmethod
    def load_diffuse_texture(diffuse_texture_path: str) -> np.ndarray:
        return np.array(PILImage.open(diffuse_texture_path).convert("RGBA"))[::-1]

    def __init__(self,
                 model_path: str = "./obj/african_head/african_head.obj",
                 diffuse_texture_path: str = "./obj/african_head/african_head_diffuse.tga"):
        vn, vt, v, f = self.parse_obj(model_path)
        self._vn = np.array(vn)
        self._vt = np.array(vt)
        self._v = np.array(v)
        self._f = np.array(f)
        self._diffuse_map = self.load_diffuse_texture(diffuse_texture_path)
        self._diffuse_width = len(self._diffuse_map[0])
        self._diffuse_height = len(self._diffuse_map)

    def polygons(self):
        return self._f

    def diffuse(self, x, y):
        return self._diffuse_map[y, x]

    def vertex(self, i):
        return self._v[i]

    def intensity(self, i):
        return self._vn[i]

    def polygon(self, i):
        return self._f[i]

    def texture_coordinates(self, i, j) -> np.ndarray:
        return self._vt[self._f[i, j, 1]] * [self._diffuse_width, self._diffuse_height, 1]
