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
        'black': (10, 10, 10),
        'cyan': (10, 245, 245),
        'yellow': (245, 245, 10),
        'magenta': (245, 10, 245)
    }
    circles = [(425, 600, 50, 'magenta'), (450, 600, 50, 'cyan'), (475, 600, 50, 'black'), (400, 600, 50, 'yellow')]

    for i in range(image.width):
        for j in range(image.height):
            for circle in circles:
                draw_circle(img, i, j, circle, colors)

    img.show()


def draw_circle(img, i, j, circle, colors):
    distance = ((i - circle[0]) ** 2 + (j - circle[1]) ** 2) ** 0.5
    radius = circle[2]
    if distance < radius:
        old_color = img.getpixel((i, j))
        distance_part = distance / radius
        density = - distance_part ** 6 + 1
        new_color = colors[circle[3]]
        new_color = tuple([int(255 - ((255 - i) * density)) for i in new_color])

        if old_color == (255, 255, 255):
            img.putpixel((i, j), new_color)
        else:
            mixed_color = tuple([min(x) for x in zip(old_color, new_color)])
            img.putpixel((i, j), mixed_color)


if __name__ == "__main__":
    main()
