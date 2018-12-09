import pathlib
import sys
from random import randrange
from typing import Tuple, List

import pygame

from src.bug import Bug
from src.board import Tile, NUMBER_OF_ROWS, NUMBER_OF_COLUMNS, BOARD_LIMITS_COLOR
from src.window import Window

WINDOW = WIN_WIDTH, WIN_HEIGHT = 800, 840
HEIGHT_OFFSET = 0.25 * WIN_HEIGHT


def draw_tile_board(scr: pygame.Surface, board: List[Tile], active_bugs: List[Bug]):
    limit_board: pygame.Rect = [0, HEIGHT_OFFSET, WIN_WIDTH, 0.75 * WIN_HEIGHT]
    pygame.draw.rect(scr, BOARD_LIMITS_COLOR, limit_board, 1)
    for tile in board:
        tile.draw_tile(scr, Bug.BOARD_OPENER in active_bugs)


def alter_position(position: Tuple[int, int]) -> Tuple[int, int]:
    x_coord = position[0]
    y_coord = position[1]

    if Bug.HORIZONTAL_TILE_TRANSLATOR in on_play_bugs:
        x_coord = (x_coord + 4 * Tile.TILE_WIDTH) % WIN_WIDTH
    if Bug.VERTICAL_TILE_TRANSLATOR in on_play_bugs:
        y_coord = (y_coord + 4 * Tile.TILE_HEIGHT) % WIN_HEIGHT
    if Bug.HORIZONTAL_TILE_REVERTER in on_play_bugs:
        x_coord = WIN_WIDTH - x_coord
    if Bug.VERTICAL_TILE_REVERTER in on_play_bugs:
        y_coord = WIN_HEIGHT - y_coord + HEIGHT_OFFSET

    return x_coord, y_coord


def mouse_clicked(board: List[Tile], position: Tuple[int, int]) -> Bug:
    buggy_position = alter_position(position)
    for tile in board:
        if tile.is_in_range(buggy_position):
            if tile.bug != Bug.NO_BUG and not tile.found_bug and tile.bug != Bug.FAKE_BUG:
                bug = on_play_bugs[0]
                print(f'bug {bug} found')
                tile.found_bug = True
                tile.opened = True
                return bug
            tile.opened = True
    return Bug.NO_BUG


def board_init() -> List[Tile]:
    board: List[Tile] = []
    for row in range(0, NUMBER_OF_ROWS):
        for column in range(0, NUMBER_OF_COLUMNS):
            position = row * Tile.TILE_WIDTH, HEIGHT_OFFSET + column * Tile.TILE_HEIGHT
            created_tile = Tile(height_offset=HEIGHT_OFFSET, position=position)
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


def bug_mover(board: List[Tile]):
    for tile in board:
        if tile.bug != Bug.NO_BUG and not tile.opened:
            number_attempts = 10
            position = randrange(NUMBER_OF_ROWS * NUMBER_OF_COLUMNS - 1)
            while (board[position].bug != Bug.NO_BUG or board[position].opened) and number_attempts > 0:
                position = randrange(NUMBER_OF_ROWS * NUMBER_OF_COLUMNS - 1)
                number_attempts -= 1
            if number_attempts:
                board[position].bug = tile.bug
                tile.bug = Bug.NO_BUG


def bug_faker(board: List[Tile]):
    for tile in board:
        if tile.bug == Bug.NO_BUG and not tile.opened:
            tile.bug = Bug.FAKE_BUG
            return


def bug_tile_closer(board: List[Tile]) -> Bug:
    for tile in board:
        if tile.opened:
            tile.opened = False
            if tile.bug != Bug.NO_BUG and tile.bug != Bug.FAKE_BUG:
                tile.found_bug = False
                return tile.bug
            return Bug.NO_BUG
    return Bug.NO_BUG


window = Window(WIN_WIDTH, WIN_HEIGHT, 'Bugs on the desert')
text_surface: pygame.Surface = window.render_text('Click on the bugs!')
Tile.set_tile_size(window_size=window.size, height_offset=HEIGHT_OFFSET)

playing_board: List[Tile] = board_init()
on_play_bugs: List[Bug] = bug_init(playing_board)
found_bugs: List[Bug] = []

window.background_image = pathlib.Path('resources/background.jpg')
bug_mover_counter = 5
bug_faker_counter = 2
bug_tile_closer_counter = 5
bug_found = Bug.NO_BUG
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            bug_found = mouse_clicked(playing_board, event.pos)
            if bug_found != Bug.NO_BUG:
                on_play_bugs.remove(bug_found)
                found_bugs.append(bug_found)
            if Bug.BUG_MOVER in on_play_bugs:
                if bug_mover_counter > 0:
                    bug_mover_counter -= 1
                else:
                    bug_mover(playing_board)
                    bug_mover_counter = 5
            if Bug.BUG_FAKER in on_play_bugs:
                if bug_faker_counter > 0:
                    bug_faker_counter -= 1
                else:
                    bug_faker(playing_board)
                    bug_faker_counter = 2
            if Bug.TILE_CLOSER in on_play_bugs:
                if bug_tile_closer_counter > 0:
                    bug_tile_closer_counter -= 1
                else:
                    bug = bug_tile_closer(playing_board)
                    bug_tile_closer_counter = 5
                    if bug != Bug.NO_BUG and bug != Bug.FAKE_BUG:
                        bug = found_bugs[len(found_bugs) - 1]
                        found_bugs.remove(bug)
                        on_play_bugs = [bug] + on_play_bugs

    window.draw_background()

    window.draw_surface(text_surface, (50, 50))

    if not len(on_play_bugs):
        bug_text_surface: pygame.Surface = window.render_text(f'No bugs left! Congratulations!')
        window.draw_surface(bug_text_surface, (50, 80))
    elif bug_found != Bug.NO_BUG:
        bug_text_surface: pygame.Surface = window.render_text(f'Bug {bug_found} found!')
        window.draw_surface(bug_text_surface, (50, 80))

    draw_tile_board(window.screen, board=playing_board, active_bugs=on_play_bugs)
    window.update()
