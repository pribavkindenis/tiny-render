from render.image import Image
from render.render import render_model
from model.model import Model


if __name__ == '__main__':
    model = Model("./obj/african_head.obj")
    image = Image(600, 600)
    render_model(model, image)
    image.save_image()
