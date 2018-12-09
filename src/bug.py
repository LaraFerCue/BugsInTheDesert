from enum import Enum


class Bug(Enum):
    BOARD_OPENER = 0
    HORIZONTAL_TILE_TRANSLATOR = 1
    VERTICAL_TILE_TRANSLATOR = 2
    HORIZONTAL_TILE_REVERTER = 3
    VERTICAL_TILE_REVERTER = 4
    BUG_MOVER = 5
    BUG_FAKER = 6
    TILE_CLOSER = 7
    FAKE_BUG = 99
    NO_BUG = -1

    def __str__(self):
        return self.name