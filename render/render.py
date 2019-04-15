from render.color import Color
from render.image import Image
from model.model import Model
import numpy as np
import sys
from typing import *


def render_model(model: Model,
                 image: Image,
                 light_direction: np.ndarray):
    light_direction = light_direction / np.linalg.norm(light_direction)

    z_buffer = np.full((image.width(), image.height()), -sys.maxsize-1)

    for i in range(len(model.polygons())):
        polygon = model.polygon(i)
        screen_coordinates = []
        world_coordinates = []
        for j in range(3):
            world_coordinates.append(model.vertex(polygon[j][0]))
            screen_coordinates.append([
                int((world_coordinates[j][0] + 1) * (image.width() / 2 - 2)),
                int((world_coordinates[j][1] + 1) * (image.height() / 2 - 2)),
                int((world_coordinates[j][2] + 1) * (image.depth() / 2 - 2))
            ])
        vector_prod = np.cross(
            world_coordinates[2] - world_coordinates[0],
            world_coordinates[1] - world_coordinates[0]
        )

        normal = vector_prod / np.linalg.norm(vector_prod)
        intensity = normal.dot(light_direction)

        if intensity > 0:
            draw_triangle(
                screen_coordinates[0],
                screen_coordinates[1],
                screen_coordinates[2],
                model.texture_coordinates(i, 0),
                model.texture_coordinates(i, 1),
                model.texture_coordinates(i, 2),
                z_buffer,
                image,
                model,
                intensity
            )


def draw_triangle(p1: List[int],
                  p2: List[int],
                  p3: List[int],
                  t1: np.ndarray,
                  t2: np.ndarray,
                  t3: np.ndarray,
                  z_buffer: np.ndarray,
                  image: Image,
                  model: Model,
                  intensity: float):
    if p1[1] == p2[1] and p1[1] == p3[1]:
        return

    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)

    if p1[1] > p2[1]:
        p1, p2 = p2, p1
        t1, t2 = t2, t1
    if p1[1] > p3[1]:
        p1, p3 = p3, p1
        t1, t3 = t3, t1
    if p2[1] > p3[1]:
        p2, p3 = p3, p2
        t2, t3 = t3, t2

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
        if a[0] > b[0]:
            a, b = b, a
            t_a, t_b = t_b, t_a
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
            if z_buffer[p[0], p[1]] < p[2]:
                z_buffer[p[0], p[1]] = p[2]
                color = Color(*model.diffuse(t_p[0], t_p[1]), intensity=intensity)
                image[p[0], p[1]] = color


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
            error -= 2*dx
