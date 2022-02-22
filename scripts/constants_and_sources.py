import pygame
display_width, display_height = (1440, 800)

directions = 'left right up down'.split()
opposites = ['right', 'left', 'dowm', 'up']

heretic_images = {i: pygame.image.load(f'../images/heretic_sprite_{i}.png') for i in directions}

BLACK = (0, 0, 0)
WHITE = '#FFFFFF'
RED = '#FF0000'
GREEN = '#00FF00'
BLUE = '#0000FF'