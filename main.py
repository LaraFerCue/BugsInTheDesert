import sys
from typing import Tuple, List

import pygame

BOARD_LIMITS_COLOR = 155, 0, 0
WINDOW = WIN_WIDTH, WIN_HEIGHT = 800, 800
NUMBER_OF_ROWS = 8
NUMBER_OF_COLUMNS = 8
HEIGHT_OFFSET = 0.25 * WIN_HEIGHT


class Tile:
    CLOSED_TILE_COLOR = [252, 166, 255]
    OPEN_TILE_COLOR = [252, 255, 166, 0]
    TILE_WIDTH = WIN_WIDTH / NUMBER_OF_COLUMNS
    TILE_HEIGHT = WIN_HEIGHT / NUMBER_OF_ROWS

    def __init__(self):
        self.opened: bool = False
        self.position: Tuple[int, int] = (0, 0)

    def draw_tile(self, scr: pygame.Surface):
        board_rect = [self.position[0], self.position[1], self.position[0] + Tile.TILE_WIDTH,
                      self.position[1] + Tile.TILE_HEIGHT]

        rect: pygame.Surface = pygame.Surface((Tile.TILE_WIDTH, Tile.TILE_HEIGHT))
        if self.opened:
            rect.set_alpha(12)
            rect.fill(Tile.OPEN_TILE_COLOR)
            scr.blit(rect, self.position)
        else:
            rect.fill(Tile.CLOSED_TILE_COLOR)
            scr.blit(rect, self.position)
        pygame.draw.rect(scr, BOARD_LIMITS_COLOR, board_rect, 1)

    def is_in_range(self, position: Tuple[int, int]) -> bool:
        if position[0] < self.position[0] or position[0] > self.position[0] + Tile.TILE_WIDTH:
            return False
        if position[1] < self.position[1] or position[1] > self.position[1] + Tile.TILE_HEIGHT:
            return False
        return True


def draw_tile_board(scr: pygame.Surface, board: List[Tile]):
    limit_board: pygame.Rect = [0, HEIGHT_OFFSET, WIN_WIDTH, 0.75 * WIN_HEIGHT]
    pygame.draw.rect(scr, BOARD_LIMITS_COLOR, limit_board, 1)
    for tile in board:
        tile.draw_tile(scr)


def mouse_clicked(board: List[Tile], position: Tuple[int, int]):
    for tile in board:
        if tile.is_in_range(position):
            tile.opened = True


playing_board: List[Tile] = []
for row in range(0, NUMBER_OF_ROWS):
    for column in range(0, NUMBER_OF_COLUMNS):
        created_tile = Tile()
        created_tile.position = row * Tile.TILE_WIDTH, HEIGHT_OFFSET + column * Tile.TILE_HEIGHT
        playing_board.append(created_tile)

pygame.init()

screen: pygame.Surface = pygame.display.set_mode(WINDOW)
pygame.display.set_caption('Bugs on the desert')
bg_image = pygame.image.load('resources/background.jpg').convert()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_clicked(playing_board, event.pos)
    screen.fill(color=(255, 255, 255))
    screen.blit(bg_image, [0, 0])

    draw_tile_board(screen, board=playing_board)
    pygame.display.flip()
