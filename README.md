# BugsInTheDesert
A python game done on the Berlin MiniGame Jam on the 08.12.2018

The objective of the game is to find on the board the eight bugs hidden on the board,
each bug creates a "unexpected" behavior on the tile.

The bugs implemented on the game are:
- Board opener: This bug inverts the status of the tiles, the closed tiles appear open and the other way around.
- Horizontal translator: This bug translates the click event 4 tiles to the right on the board.
- Vertical translator: This bug translates the click event 4 tiles down on the board.
- Horizontal reflector: This bug reflects the click horizontally on the board.
- Vertical reflector: This bug reflects the click vertically on the board.
- Bug Mover: Moves each 5 clicks the bugs around on the board.
- Bug Faker: Creates fake bugs on the board each two clicks.
- Tile closer: Closes the first open tile on the board each two clicks and, if a bug is found on the tile, it will be activated again.

Important information:
At first, ALL the bugs are active at the same time, meaning that a click on a tile will happen four mirrored and
translated on the board, each two clicks a new fake bug will appear on the board and a tile will be closed, and each
five turns, the bugs will be moving around on the board.