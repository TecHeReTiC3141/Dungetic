import pygame
display_width, display_height = (1440, 800)

direction = 'left right up down'.split()

heretic_images = {i: pygame.image.load(f'../images/heretic_sprite_{i}.png') for i in direction}

print(heretic_images)