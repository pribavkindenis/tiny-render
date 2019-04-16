from render.image import Image
from render.render import render_model
from model.model import Model
import numpy as np


def render(model: Model, save_path: str):
    image = Image(800, 800)
    render_model(model,
                 image,
                 np.array([0, 0, 1]),
                 np.array([2, 0.5, 5]),
                 np.array([0, 0, 0]))
    image.save_image(save_path)


if __name__ == '__main__':
    render(Model(), "african_head.png")
    render(Model("./obj/diablo/diablo.obj", "./obj/diablo/diablo_diffuse.tga"), "diablo.png")
