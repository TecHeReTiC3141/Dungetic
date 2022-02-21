import pygame
from classes.Heretic import Heretic

display_width, display_height = (640, 480)

display = pygame.display.set_mode((display_width, display_height))
heretic = Heretic(100, 100, 75, 100, 78, None, [])

direction = 'left right up down'.split()

clock = pygame.time.Clock()

for dir in direction:
    heretic.direction = dir

    display.fill((218, 150, 61))
    heretic.draw_object(display)
    pygame.image.save(heretic.visible_zone, f'heretic_sprite_{dir}.png')
    pygame.display.update()

    clock.tick(60)
