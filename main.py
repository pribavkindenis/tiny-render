from render.image import Image

if __name__ == '__main__':
    img = Image(1920, 1080)
    img[:, :] = [255, 255, 0, 255]
    img.save_image()


