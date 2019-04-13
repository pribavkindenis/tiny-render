from render.image import Image
from render.color import Color

if __name__ == '__main__':
    img = Image(1920, 1080)
    img[:, :] = Color(255, 255, 0, 255)
    img.save_image()


