import sys
from enum import Enum
from random import randrange
from typing import Tuple, List

import pygame

BOARD_LIMITS_COLOR = 155, 0, 0
WINDOW = WIN_WIDTH, WIN_HEIGHT = 800, 820
NUMBER_OF_ROWS = 8
NUMBER_OF_COLUMNS = 8
HEIGHT_OFFSET = 0.25 * WIN_HEIGHT


# Bugs to be fixed:
# - A bug makes all the tiles open -> closes the tiles
# - A bug makes the bugs move around -> bugs will be in fixed positions
# - A bug makes the click events to translate a number of tiles horizontally
# - A bug makes the click events to translate a number of tiles vertically
# - A bug makes the click events to be reverted on the board horizontally
# - A bug makes the click events to be reverted on the board vertically
# - A bug creates fake bug tiles
# - A bug closes tiles
class Bug(Enum):
    BOARD_OPENER = 0
    BUG_MOVER = 1
    HORIZONTAL_TILE_TRANSLATOR = 2
    VERTICAL_TILE_TRANSLATOR = 3
    HORIZONTAL_TILE_REVERTER = 4
    VERTICAL_TILE_REVERTER = 5
    BUG_FAKER = 6
    TILE_CLOSER = 7
    FAKE_BUG = 99
    NO_BUG = -1


class Tile:
    FAKE_BUG_COLOR = [100, 0, 0]
    BUG_COLOR = [255, 0, 0]
    CLOSED_TILE_COLOR = [252, 166, 255]
    OPEN_TILE_COLOR = [252, 255, 166, 0]
    TILE_WIDTH = WIN_WIDTH / NUMBER_OF_COLUMNS
    TILE_HEIGHT = (WIN_HEIGHT - HEIGHT_OFFSET) / NUMBER_OF_ROWS

    def __init__(self):
        self.opened: bool = False
        self.position: Tuple[int, int] = (0, 0)
        self.bug: Bug = Bug.NO_BUG

    @property
    def bug_position(self) -> Tuple[int, int]:
        bug_pos_x = int(self.position[0] + Tile.TILE_WIDTH / 2)
        bug_pos_y = int(self.position[1] + Tile.TILE_HEIGHT / 2)
        return bug_pos_x, bug_pos_y

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

        if self.bug != Bug.NO_BUG:
            if self.bug == Bug.FAKE_BUG:
                pygame.draw.circle(scr, Tile.FAKE_BUG_COLOR, self.bug_position, int(Tile.TILE_WIDTH / 4))
            print(f'printing bug {self.bug} on {self.bug_position} size {Tile.TILE_WIDTH / 4}')
            pygame.draw.circle(scr, Tile.BUG_COLOR, self.bug_position, int(Tile.TILE_WIDTH / 4))
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
            return None


def board_init() -> List[Tile]:
    board: List[Tile] = []
    for row in range(0, NUMBER_OF_ROWS):
        for column in range(0, NUMBER_OF_COLUMNS):
            created_tile = Tile()
            created_tile.position = row * Tile.TILE_WIDTH, HEIGHT_OFFSET + column * Tile.TILE_HEIGHT
            board.append(created_tile)

    return board


def bug_init(board: List[Tile]) -> List[Bug]:
    bugs: List[Bug] = []
    tiles_used: List[int] = []
    for bug in range(0, 8):
        bugs.append(Bug(bug))
        position = randrange(NUMBER_OF_COLUMNS * NUMBER_OF_ROWS)
        while position in tiles_used:
            position = randrange(NUMBER_OF_COLUMNS * NUMBER_OF_ROWS)
        board[position].bug = Bug(bug)
        tiles_used.append(position)
    return bugs


playing_board: List[Tile] = board_init()
on_play_bugs: List[Bug] = bug_init(playing_board)
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
