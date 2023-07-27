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

    colors = {
        'black': (0, 0, 0),
        'cyan': (0, 255, 255),
        'yellow': (255, 255, 0),
        'magenta': (255, 0, 255)
    }
    circles = [(425, 600, 50, 'magenta'), (450, 600, 50, 'cyan'), (475, 600, 50, 'black'), (400, 600, 50, 'yellow')]

    for i in range(image.width):
        for j in range(image.height):
            for circle in circles:
                if ((i - circle[0]) ** 2 + (j - circle[1]) ** 2) ** 0.5 < circle[2]:
                    old_color = img.getpixel((i, j))
                    new_color = colors[circle[3]]
                    if old_color == (255, 255, 255):
                        img.putpixel((i, j), new_color)
                    else:
                        mixed_color = tuple([int((min(x) + sum(x) / 2) / 2) for x in zip(old_color, new_color)])
                        img.putpixel((i, j), mixed_color)

    img.show()


if __name__ == "__main__":
    main()
