from typing import Tuple, List

from src.board import Tile
from src.bug import Bug


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
                tile.opened = True
                return bug
            tile.opened = True
    return Bug.NO_BUG
