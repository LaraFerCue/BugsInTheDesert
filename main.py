import sys

import pygame

BOARD_LIMITS_COLOR = 155, 0, 0
WINDOW = WIN_WIDTH, WIN_HEIGHT = 800, 800
NUMBER_OF_ROWS = 8
NUMBER_OF_COLUMNS = 8


def draw_tile_board(scr: pygame.Surface):
    tile_width = WIN_WIDTH / NUMBER_OF_COLUMNS
    tile_height = WIN_HEIGHT / NUMBER_OF_ROWS

    height_offset = 0.25 * WIN_HEIGHT
    playing_board: pygame.Rect = [0, height_offset, WIN_WIDTH, 0.75 * WIN_HEIGHT]
    pygame.draw.rect(scr, BOARD_LIMITS_COLOR, playing_board, 1)

    for row in range(0, NUMBER_OF_ROWS):
        for column in range(0, NUMBER_OF_COLUMNS):
            tile_rect: pygame.Rect = [row * tile_width, height_offset + column * tile_height, (row + 1) * tile_width,
                                      height_offset + (column + 1) * tile_height]
            pygame.draw.rect(scr, BOARD_LIMITS_COLOR, tile_rect, 1)


pygame.init()

screen: pygame.Surface = pygame.display.set_mode(WINDOW)
pygame.display.set_caption('Bugs on the desert')
# bg_image = pygame.image.load('resources/background.jpg').convert()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    # screen.blit(bg_image, [0, 0])

    screen.fill(color=(255, 255, 255))
    draw_tile_board(screen)
    pygame.display.flip()
