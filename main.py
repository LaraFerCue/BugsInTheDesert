import pathlib
import sys
from random import randrange
from typing import List

import pygame

from src import events
from src.board import Tile, NUMBER_OF_ROWS, NUMBER_OF_COLUMNS, draw_tile_board
from src.bug import Bug
from src.events import alter_position, mouse_clicked
from src.window import Window

WINDOW = WIN_WIDTH, WIN_HEIGHT = 800, 840
HEIGHT_OFFSET = 0.25 * WIN_HEIGHT


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


window = Window(WIN_WIDTH, WIN_HEIGHT, 'Bugs on the desert')
text_surface: pygame.Surface = window.render_text('Click on the bugs!')
Tile.set_tile_size(window_size=window.size, height_offset=HEIGHT_OFFSET)

playing_board: List[Tile] = board_init()
on_play_bugs: List[Bug] = bug_init(playing_board)

window.background_image = pathlib.Path('resources/background.jpg')
bug_found = Bug.NO_BUG

event_list: List[events.Event] = {
    events.BugMoverEvent(5),
    events.BugFakerEvent(2),
    events.BugTileCloserEvent(5)
}

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = alter_position(position=event.pos, active_bugs=on_play_bugs, win_size=window.size,
                                 height_offset=HEIGHT_OFFSET)
            bug_found = mouse_clicked(playing_board, pos, active_bugs=on_play_bugs)

            for bug_event in event_list:
                on_play_bugs = bug_event.action(playing_board, on_play_bugs)

    window.draw_background()

    window.draw_surface(text_surface, (50, 50))

    if not len(on_play_bugs):
        bug_text_surface: pygame.Surface = window.render_text(f'No bugs left! Congratulations!')
        window.draw_surface(bug_text_surface, (50, 80))
    elif bug_found != Bug.NO_BUG:
        bug_text_surface: pygame.Surface = window.render_text(f'Bug {bug_found} found!')
        window.draw_surface(bug_text_surface, (50, 80))

    draw_tile_board(window, board=playing_board, active_bugs=on_play_bugs, height_offset=HEIGHT_OFFSET)
    window.update()
