from typing import Tuple, List

import pygame

from src.bug import Bug

NUMBER_OF_ROWS = 8
NUMBER_OF_COLUMNS = 8
BOARD_LIMITS_COLOR = 155, 0, 0


class Tile:
    FAKE_BUG_COLOR = [100, 0, 0]
    BUG_COLOR = [255, 0, 0]
    CLOSED_TILE_COLOR = [252, 166, 255]
    OPEN_TILE_COLOR = [252, 255, 166, 0]
    TILE_WIDTH = 0
    TILE_HEIGHT = 0

    def __init__(self,  height_offset: int, position: Tuple[int, int]):
        self.opened: bool = False
        self.position: Tuple[int, int] = position
        self.bug: Bug = Bug.NO_BUG
        self.found_bug: bool = False
        self.height_offset: int = height_offset

    @property
    def bug_position(self) -> Tuple[int, int]:
        bug_pos_x = self.position[0] + 5
        bug_pos_y = self.position[1] + 5
        return bug_pos_x, bug_pos_y

    @property
    def tile_size(self) -> Tuple[int, int]:
        return Tile.TILE_WIDTH, Tile.TILE_HEIGHT

    def draw_tile(self, scr: pygame.Surface, on_play_bugs: List[Bug]):
        board_rect = [self.position[0], self.position[1], Tile.TILE_WIDTH, Tile.TILE_HEIGHT]

        rect: pygame.Surface = pygame.Surface(self.tile_size)
        if (Bug.BOARD_OPENER in on_play_bugs and not self.opened) or (
                self.opened and Bug.BOARD_OPENER not in on_play_bugs):
            rect.set_alpha(12)
            rect.fill(Tile.OPEN_TILE_COLOR)
            scr.blit(rect, self.position)
            if self.bug != Bug.NO_BUG:
                if self.bug == Bug.FAKE_BUG:
                    bug_image = pygame.image.load('resources/fake_bug.gif').convert()
                else:
                    bug_image = pygame.image.load('resources/bug.gif').convert()
                scr.blit(bug_image, self.bug_position)
        else:
            tile_image = pygame.image.load('resources/tile.gif').convert()
            scr.blit(tile_image, self.position)

        pygame.draw.rect(scr, BOARD_LIMITS_COLOR, board_rect, 1)

    def is_in_range(self, position: Tuple[int, int]) -> bool:
        if position[0] < self.position[0] or position[0] > self.position[0] + Tile.TILE_WIDTH:
            return False
        if position[1] < self.position[1] or position[1] > self.position[1] + Tile.TILE_HEIGHT:
            return False
        return True

    @staticmethod
    def set_tile_size(window_size: Tuple[int, int], height_offset: int):
        Tile.TILE_WIDTH = int(window_size[0] / NUMBER_OF_COLUMNS)
        Tile.TILE_HEIGHT = int((window_size[1] - height_offset) / NUMBER_OF_ROWS)
