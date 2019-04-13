from render.image import Image
from render.render import render_model
from model.model import Model
from render.color import Color
import numpy as np


if __name__ == '__main__':
    model = Model("./obj/african_head.obj")
    image = Image(3000, 3000)
    render_model(model, image, np.array([0, 0, 1]), Color(101, 36, 127))
    image.save_image()
