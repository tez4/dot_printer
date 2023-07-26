import attr
import math
import pygame
import random
import numpy as np
import pygame_widgets
from typing import Union, Optional, Any
from PIL import Image, ImageDraw, ImageFont
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox


@attr.s
class Program:
    screen_width: int = attr.ib(
        validator=attr.validators.instance_of(int),
        on_setattr=attr.setters.validate)
    screen_height: int = attr.ib(
        validator=attr.validators.instance_of(int),
        on_setattr=attr.setters.validate)
    running: Any = attr.ib(default=True)
    screen: Any = attr.ib(default=None)
    image: str = attr.ib(default="./assets/test_image_04.jpg")

    def __attrs_post_init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.screen_height = self.screen.get_height()
        # self.screen_width = self.screen.get_width()

        pygame.display.set_caption("Dot Printer")
        icon = pygame.image.load("./assets/spaceship.png")
        pygame.display.set_icon(icon)
        image = Image.open(self.image)

        while self.running:
            self.run_program_loop(image)

    def run_program_loop(self, image):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.screen_height = self.screen.get_height()
                self.screen_width = self.screen.get_width()

        self.screen.fill('#FFFFFF')
        RADIUS = 2
        density = 50

        draw_radius = max(image.width, image.height)
        num_of_circles = int(np.ceil(draw_radius / density))

        print(image.width)

        colors = [(0, 0, 0, 128), (0, 255, 255, 128), (255, 255, 0, 128), (255, 0, 255, 128)]
        circle_surfaces = []
        for color, index in zip(colors, [0, 1, 2, 3]):
            for i in range(num_of_circles):
                for j in range(num_of_circles):
                    my_i = i - (num_of_circles / 2)
                    my_j = j - (num_of_circles / 2)
                    angle = index * -0.3926875  # radiens
                    x = my_i * np.cos(angle) - my_j * np.sin(angle)
                    y = my_i * np.sin(angle) + my_j * np.cos(angle)
                    circle_surface = pygame.Surface((2 * RADIUS, 2 * RADIUS), pygame.SRCALPHA)
                    pygame.draw.circle(circle_surface, color, (RADIUS, RADIUS), RADIUS)
                    circle_surfaces.append((circle_surface, (600 + x * 10, 400 + y * 10)))

        for circle_surface, position in circle_surfaces:
            self.screen.blit(circle_surface, position)

        pygame_widgets.update(events)
        pygame.display.update()


if __name__ == '__main__':
    image_editor = Program(1200, 800)
