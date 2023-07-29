import attr
import math
import random
# import cairosvg
import datetime
import colorsys
import svgwrite
import numpy as np
from io import BytesIO
from typing import Union, Optional, Any
from PIL import Image, ImageDraw, ImageFont


def main():
    image = read_image(size_increase=4)
    draw_image(image, density=20, mode='jpg')


def read_image(name="./assets/test_image_03.jpg", size_increase=2):
    image = Image.open(name)
    image = image.resize((image.width * size_increase, image.height * size_increase))
    return image


def draw_image(image, density, mode='jpg'):

    colors = {
        'black': (10, 10, 10),
        'cyan': (10, 245, 245),
        'yellow': (245, 245, 10),
        'magenta': (245, 10, 245)
    }
    # circles = [(425, 600, 50, 'magenta'), (450, 600, 50, 'cyan'), (475, 600, 50, 'black'), (400, 600, 50, 'yellow')]
    circles = get_circle_data(image, colors, density)
    print(f'Circles: {len(circles)}')

    if mode == 'jpg':
        jpg_images = {}
        jpg_draws = {}
        for color in colors.keys():
            img = Image.new('RGB', (image.width, image.height), color='#FFFFFF')
            jpg_images[color] = img
            jpg_draws[color] = ImageDraw.Draw(img)
        for circle_number, circle in enumerate(circles):
            upper_left = (circle[0] - circle[2], circle[1] - circle[2])
            lower_right = (circle[0] + circle[2], circle[1] + circle[2])
            jpg_draws[circle[3]].ellipse([upper_left, lower_right], fill=circle[3])
            print(f'{circle_number + 1} / {len(circles)} circles drawn.')

        image = np.ones_like(np.array(jpg_images['black']), dtype=np.float64)
        for color in colors.keys():
            image *= np.array(jpg_images[color]) / 255

        image *= 255
        pil_image = Image.fromarray(image.astype(np.uint8))
        name = f'./output/{random.randint(1,100000)}.jpg'
        pil_image.save(name)
        print(f'Done! Saved image as {name}')

        # for i in range(max(int(circle[0] - circle[2]), 0), min(int(circle[0] + circle[2]), image.width)):
        #     for j in range(max(int(circle[1] - circle[2]), 0), min(int(circle[1] + circle[2]), image.height)):
        #         draw_circle(img, i, j, circle, colors)
        # img.show()

    elif mode == 'svg':

        # write svg images
        svg_images = {}
        for color in colors.keys():
            svg_images[color] = svgwrite.Drawing(f'./output/{color}.svg', (image.width, image.height))
        for circle in circles:
            svg_images[circle[3]].add(
                svgwrite.shapes.Circle(
                    center=(circle[0], circle[1]),
                    r=circle[2],
                    fill=svgwrite.rgb(*colors[circle[3]])
                )
            )
        for svg in svg_images.values():
            svg.save()

        # convert to jpg
        # png_data = cairosvg.svg2png(url="./output/magenta.svg")
        # image = Image.open(BytesIO(png_data))


def rgb_to_cmyk(r, g, b):
    CMYK_SCALE = 100
    RGB_SCALE = 255

    if (r, g, b) == (0, 0, 0):
        # black
        return 0, 0, 0, CMYK_SCALE

    # rgb [0,255] -> cmy [0,1]
    c = 1 - r / RGB_SCALE
    m = 1 - g / RGB_SCALE
    y = 1 - b / RGB_SCALE

    # extract out k [0, 1]
    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy

    # rescale to the range [0,CMYK_SCALE]
    return c * CMYK_SCALE, m * CMYK_SCALE, y * CMYK_SCALE, k * CMYK_SCALE


def get_circle_data(image, colors, density):
    circles = []
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

                rgb_color = image.getpixel((x_image_pixel, y_image_pixel))
                cyan, magenta, yellow, black = rgb_to_cmyk(*rgb_color)
                if direction_index == 0:
                    color_size = black
                elif direction_index == 1:
                    color_size = cyan
                elif direction_index == 2:
                    color_size = yellow
                else:
                    color_size = magenta

                color_size = ((color_size / 100) ** 0.5) / 2

                circles.append((x_image_pixel, y_image_pixel, density * color_size, color))

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
            mixed_color = tuple([255 - min((255 - x) + (255 - y), 255) for x, y in zip(old_color, new_color)])
            img.putpixel((i, j), mixed_color)


if __name__ == "__main__":
    main()
