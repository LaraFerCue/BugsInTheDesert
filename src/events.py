from random import randrange
from typing import Tuple, List

from src.board import Tile
from src.bug import Bug


def get_random_board_position(board: List[Tile], with_bug: bool = False, must_be_closed: bool = False):
    position = randrange(len(board) - 1)
    number_of_attempts = 10

    tile = board[position]
    while (tile.bug != Bug.NO_BUG) != with_bug or (tile.is_open and must_be_closed) and number_of_attempts > 0:
        position = randrange(len(board) - 1)
        tile = board[position]
        number_of_attempts -= 1

    return position if number_of_attempts else -1


class Event:
    def __init__(self, counter: int = -1):
        self._counter: int = counter
        self._iter: int = 0

    def action(self, board: List[Tile], active_bugs: List[Bug]) -> List[Bug]:
        pass


class BugMoverEvent(Event):
    def action(self, board: List[Tile], active_bugs: List[Bug]) -> List[Bug]:
        if Bug.BUG_MOVER not in active_bugs:
            return active_bugs

        if self._iter < self._counter:
            self._iter += 1
        else:
            self._iter = 0
            for tile in board:
                if tile.bug != Bug.NO_BUG and not tile.is_open:
                    position = get_random_board_position(board, False, True)
                    if position >= 0:
                        board[position].bug = tile.bug
                        tile.bug = Bug.NO_BUG
        return active_bugs


class BugFakerEvent(Event):
    def action(self, board: List[Tile], active_bugs: List[Bug]) -> List[Bug]:
        if Bug.BUG_FAKER not in active_bugs:
            return active_bugs

        if self._iter < self._counter:
            self._iter += 1
        else:
            self._iter = 0
            position = get_random_board_position(board, False, False)
            board[position].bug = Bug.FAKE_BUG
        return active_bugs


class BugTileCloserEvent(Event):
    def action(self, board: List[Tile], active_bugs: List[Bug]) -> List[Bug]:
        if Bug.BOARD_OPENER not in active_bugs:
            return active_bugs

        if self._iter < self._counter:
            self._iter += 1
        else:
            self._iter = 0
            for tile in board:
                if tile.is_open:
                    tile.is_open = False
                    if tile.bug != Bug.NO_BUG and Bug.FAKE_BUG:
                        found_bug = Bug(active_bugs[0].value - 1)
                        tile.found_bug = False
                        return [found_bug] + active_bugs
                    return active_bugs

        return active_bugs


def alter_position(position: Tuple[int, int], active_bugs: List[Bug],
                   win_size: Tuple[int, int], height_offset: int) -> Tuple[int, int]:
    x_coord = position[0]
    y_coord = position[1]

    if Bug.HORIZONTAL_TILE_TRANSLATOR in active_bugs:
        x_coord = (x_coord + 4 * Tile.TILE_WIDTH) % win_size[0]
    if Bug.VERTICAL_TILE_TRANSLATOR in active_bugs:
        y_coord = (y_coord + 4 * Tile.TILE_HEIGHT) % win_size[1]
    if Bug.HORIZONTAL_TILE_REVERTER in active_bugs:
        x_coord = win_size[0] - x_coord
    if Bug.VERTICAL_TILE_REVERTER in active_bugs:
        y_coord = win_size[1] - y_coord + height_offset

    return x_coord, y_coord


def mouse_clicked(board: List[Tile], position: Tuple[int, int], active_bugs: List[Bug]) -> Bug:
    for tile in board:
        if tile.is_in_range(position):
            if tile.bug != Bug.NO_BUG and not tile.found_bug and tile.bug != Bug.FAKE_BUG:
                bug = active_bugs[0]
                tile.found_bug = True
                tile.is_open = True
                return bug
            tile.is_open = True
    return Bug.NO_BUG
