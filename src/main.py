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

    def __attrs_post_init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.screen_height = self.screen.get_height()
        # self.screen_width = self.screen.get_width()

        pygame.display.set_caption("Bad Renderer")
        icon = pygame.image.load("./assets/spaceship.png")
        pygame.display.set_icon(icon)

        while self.running:
            self.run_program_loop()

    def run_program_loop(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.screen_height = self.screen.get_height()
                self.screen_width = self.screen.get_width()

        pygame_widgets.update(events)
        pygame.display.update()


if __name__ == '__main__':
    image_editor = Program(1200, 800)
