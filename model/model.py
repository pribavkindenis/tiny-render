from typing import *
import numpy as np


class Model:

    def __init__(self, path: str = "./obj/african_head.obj"):
        v, f = self.parse_obj(path)
        self._v = np.array(v)
        self._f = np.array(f)

    def vertexes(self):
        return self._v

    def polygons(self):
        return self._f

    def vertex(self, i):
        return self._v[i]

    def polygon(self, i):
        return self._f[i]

    @staticmethod
    def parse_obj(path) -> Tuple[List, List]:
        v = []
        f = []
        with open(path, "r") as file:
            for line in file:
                if line.startswith("vt"):
                    pass
                elif line.startswith("vn"):
                    pass
                elif line.startswith("v"):
                    Model.parse_vertex(line, v)
                elif line.startswith("f"):
                    Model.parse_polygon(line, f)
        return v, f

    @staticmethod
    def parse_vertex(line: str, array: list):
        data = line.strip().split(" ")
        result = []
        for i in range(1, len(data)):
            try:
                result.append(float(data[i]))
            except ValueError:
                raise IOError("Object file is invalid")
        array.append(result)

    @staticmethod
    def parse_polygon(line: str, array: list):
        data = line.strip().split(" ")
        result = []
        for i in range(1, 4):
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
