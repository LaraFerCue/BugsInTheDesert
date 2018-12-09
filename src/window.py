import pathlib

import pygame
from typing import Tuple


class Window:
    def __init__(self, width: int, height: int, name: str):
        self.__width: int = width
        self.__height: int = height
        self.__screen: pygame.Surface = None
        self.__font: pygame.font.Font = None
        self.__name: str = name
        self.__init_screen()
        self.__background: pygame.Surface = None

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def size(self) -> Tuple[int, int]:
        return self.width, self.height

    @property
    def screen(self) -> pygame.Surface:
        return self.__screen

    @property
    def background_image(self) -> pygame.Surface:
        return self.__background

    @background_image.setter
    def background_image(self, path_to_image: pathlib.Path):
        if not path_to_image.is_file():
            raise FileNotFoundError(f'image {path_to_image.absolute().as_posix()} not found!')
        self.__background = pygame.image.load(path_to_image.absolute().as_posix()).convert()

    def __init_screen(self):
        pygame.init()
        pygame.font.init()
        self.__font = pygame.font.SysFont('Comic Sans MS', 20)
        self.__screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.__name)

    def render_text(self, string: str) -> pygame.Surface:
        return self.__font.render(string, False, (0, 0, 0))

    def draw_surface(self, surface: pygame.Surface, position: Tuple[int, int]):
        self.__screen.blit(surface, position)

    def draw_background(self):
        self.__screen.fill((255, 255, 255))
        self.__screen.blit(self.background_image, (0, 0))

    @staticmethod
    def update():
        pygame.display.flip()
