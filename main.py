from render.image import Image
from render.render import render_model
from model.model import Model
import numpy as np


if __name__ == '__main__':
    model = Model("./obj/african_head.obj")
    image = Image(800, 800)
    render_model(model,
                 image,
                 np.array([0, 0, -1]),
                 np.array([2, 0.5, 5]),
                 np.array([0, 0, 0]))
    image.save_image()
