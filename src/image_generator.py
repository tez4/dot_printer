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
    circles = get_circle_data(image, colors)
    print(f'Circles: {len(circles)}')

    for circle_number, circle in enumerate(circles):
        for i in range(max(int(circle[0] - circle[2]), 0), min(int(circle[0] + circle[2]), image.width)):
            for j in range(max(int(circle[1] - circle[2]), 0), min(int(circle[1] + circle[2]), image.height)):
                draw_circle(img, i, j, circle, colors)
        print(f'{circle_number + 1} / {len(circles)} circles drawn.')
    img.show()


def get_circle_data(image, colors):
    circles = []
    density = 50
    draw_radius = image.width + image.height
    num_of_circles = int(np.ceil(draw_radius / density))
    for direction_index, color in enumerate(colors.keys()):
        for i in range(num_of_circles):
            for j in range(num_of_circles):
                my_i = i - (num_of_circles / 2)
                my_j = j - (num_of_circles / 2)
                angle = - direction_index * 22.5 * np.pi / 180
                x = my_i * np.cos(angle) - my_j * np.sin(angle)
                y = my_i * np.sin(angle) + my_j * np.cos(angle)

                # find where on the image the point is
                x_image_pixel = x * density + image.width / 2
                y_image_pixel = y * density + image.height / 2

                # remove points outside of image
                if x_image_pixel < 0 or x_image_pixel >= image.width:
                    continue
                if y_image_pixel < 0 or y_image_pixel >= image.height:
                    continue

                circles.append((x_image_pixel, y_image_pixel, density / 3, color))

    return circles


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
