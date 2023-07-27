import attr
import math
import random
import colorsys
import numpy as np
from typing import Union, Optional, Any
from PIL import Image, ImageDraw, ImageFont


def main():
    image = read_image()
    draw_image(image)


def read_image(name="./assets/test_image_04.jpg"):
    image = Image.open(name)
    return image


def draw_image(image):
    img = Image.new('RGB', (image.width, image.height), color='#FFFFFF')
    circle = (400, 600, 50)
    for i in range(image.width):
        for j in range(image.height):
            if ((i - circle[0]) ** 2 + (j - circle[1]) ** 2) ** 0.5 < circle[2]:
                img.putpixel((i, j), (255, 255, 0))

    img.show()


if __name__ == "__main__":
    main()
