import sys

import pygame

pygame.init()

display = pygame.display.set_mode()
pygame.display.set_caption('Bugs on the desert')
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.display.flip()
