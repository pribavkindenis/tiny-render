from render.image import Image
from render.render import render_model
from model.model import Model
import numpy as np


if __name__ == '__main__':
    model = Model("./obj/african_head.obj")
    image = Image(600, 600)
    render_model(model, image, np.array([0, 0, -1]))
    image.save_image()
