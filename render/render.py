from render.color import Color
from render.image import Image
from model.model import Model
from typing import *
import numpy as np
import sys


def get_view_port(x, y, width, height, depth):
    result = np.identity(4)

    result[0, 3] = x + width / 2
    result[1, 3] = y + height / 2
    result[2, 3] = depth / 2

    result[0, 0] = width / 2
    result[1, 1] = height / 2
    result[2, 2] = depth / 2

    return result


def to_matrix(vector: np.ndarray):
    return np.append(vector, 1)


def to_vector(matrix: np.ndarray):
    return np.delete(matrix / matrix[3], 3)


def look_at(eye: np.ndarray,
            center: np.ndarray,
            up: np.ndarray) -> np.ndarray:
    z = (eye - center)
    z = z / np.linalg.norm(z)
    x = np.cross(up, z)
    x = x / np.linalg.norm(x)
    y = np.cross(z, x)
    y = y / np.linalg.norm(y)
    minv = np.identity(4)
    tr = np.identity(4)
    for i in range(3):
        minv[0, i] = x[i]
        minv[1, i] = y[i]
        minv[2, i] = z[i]
        tr[i, 3] = -center[i]
    return minv.dot(tr)


def render_model(model: Model,
                 image: Image,
                 light_direction: np.ndarray,
                 eye: np.ndarray,
                 center: np.ndarray):
    light_direction = light_direction / np.linalg.norm(light_direction)
    z_buffer = np.full((image.width(), image.height()), -sys.maxsize - 1)
    projection = np.identity(4)
    projection[3, 2] = - 1 / np.linalg.norm(eye - center)
    model_view = look_at(eye, center, np.array([0, 1, 0]))
    view_port = get_view_port(
        image.width() / 8,
        image.width() / 8,
        image.width() * 3 / 4,
        image.height() * 3 / 4,
        image.depth())

    for i in range(len(model.polygons())):
        polygon = model.polygon(i)
        world_coordinates = model.vertex(polygon[:, 0])
        intensities = model.intensity(polygon[:, 2])
        screen_coordinates: List[np.ndarray] = [np.empty(0)] * 3
        screen_coordinates[0] = to_vector(view_port.dot(projection.dot(model_view.dot(to_matrix(world_coordinates[0]))))).round().astype(int)
        screen_coordinates[1] = to_vector(view_port.dot(projection.dot(model_view.dot(to_matrix(world_coordinates[1]))))).round().astype(int)
        screen_coordinates[2] = to_vector(view_port.dot(projection.dot(model_view.dot(to_matrix(world_coordinates[2]))))).round().astype(int)

        draw_triangle(
            screen_coordinates[0],
            screen_coordinates[1],
            screen_coordinates[2],
            model.texture_coordinates(i, 0),
            model.texture_coordinates(i, 1),
            model.texture_coordinates(i, 2),
            intensities[0],
            intensities[1],
            intensities[2],
            z_buffer,
            image,
            model,
            light_direction)


def draw_triangle(p1: np.ndarray,
                  p2: np.ndarray,
                  p3: np.ndarray,
                  t1: np.ndarray,
                  t2: np.ndarray,
                  t3: np.ndarray,
                  i1: np.ndarray,
                  i2: np.ndarray,
                  i3: np.ndarray,
                  z_buffer: np.ndarray,
                  image: Image,
                  model: Model,
                  light_direction: np.ndarray):
    if p1[1] == p2[1] and p1[1] == p3[1]:
        return

    if p1[1] > p2[1]:
        p1, p2 = p2, p1
        t1, t2 = t2, t1
        i1, i2 = i2, i1
    if p1[1] > p3[1]:
        p1, p3 = p3, p1
        t1, t3 = t3, t1
        i1, i3 = i3, i1
    if p2[1] > p3[1]:
        p2, p3 = p3, p2
        t2, t3 = t3, t2
        i2, i3 = i3, i2

    total_height = p3[1] - p1[1]
    for i in range(total_height):
        second_half = i > p2[1] - p1[1] or p2[1] == p1[1]
        segment_height = p3[1] - p2[1] if second_half else p2[1] - p1[1]
        alpha = i / total_height
        beta = (i - (p2[1] - p1[1] if second_half else 0)) / segment_height
        a = p1 + (p3 - p1) * alpha
        b = p2 + (p3 - p2) * beta if second_half else p1 + (p2 - p1) * beta
        t_a = t1 + (t3 - t1) * alpha
        t_b = t2 + (t3 - t2) * beta if second_half else t1 + (t2 - t1) * beta
        i_a = i1 + (i3 - i1) * alpha
        i_b = i2 + (i3 - i2) * beta if second_half else i1 + (i2 - i1) * beta
        if a[0] > b[0]:
            a, b = b, a
            t_a, t_b = t_b, t_a
            i_a, i_b = i_b, i_a
        a = a.round().astype(int)
        b = b.round().astype(int)
        t_a = t_a.round().astype(int)
        t_b = t_b.round().astype(int)
        for j in range(a[0], b[0] + 1):
            phi = 1.0 if b[0] == a[0] else (j - a[0]) / (b[0] - a[0])
            p = a + (b - a) * phi
            p = p.round().astype(int)
            t_p = t_a + (t_b - t_a) * phi
            t_p = t_p.round().astype(int)
            i_p = i_a + (i_b - i_a) * phi
            r = np.dot(i_p, light_direction)
            r = r if r >= 0 else 0
            if z_buffer[p[0], p[1]] < p[2]:
                z_buffer[p[0], p[1]] = p[2]
                image[p[0], p[1]] = Color(*model.diffuse(t_p[0], t_p[1]), intensity=r)


def draw_line(x0: int,
              y0: int,
              x1: int,
              y1: int,
              image: Image,
              color: Color):
    steep = False

    if abs(x0 - x1) < abs(y0 - y1):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        steep = True

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0

    d_error = 2 * abs(dy)
    error = 0
    y = y0
    for x in range(x0, x1 + 1):
        if steep:
            image[y, x] = color
        else:
            image[x, y] = color

        error += d_error
        if error > dx:
            y += 1 if y1 > y0 else -1
            error -= 2 * dx