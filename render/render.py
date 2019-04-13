from render.color import Color
from render.image import Image
from model.model import Model


def render_model(model: Model, image: Image):
    for i in range(len(model.polygons())):
        polygon = model.polygon(i)
        for j in range(3):
            vertex0 = model.vertex(polygon[j][0])
            vertex1 = model.vertex(polygon[(j+1) % 3][0])
            x0 = int((vertex0[0] + 1) * (image.width() / 2 - 2))
            y0 = int((vertex0[1] + 1) * (image.height() / 2 - 2))
            x1 = int((vertex1[0] + 1) * (image.width() / 2 - 2))
            y1 = int((vertex1[1] + 1) * (image.height() / 2 - 2))
            draw_line(x0, y0, x1, y1, image, Color(255, 255, 255, 255))


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
