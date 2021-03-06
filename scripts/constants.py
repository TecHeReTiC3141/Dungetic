from random import *
from pathfinding.core.grid import Grid, Node
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
from collections import *
import PySimpleGUI as sg
from scripts.Maths import *
from scripts.log_sets import logging
import pickle
from time import *
from pathlib import Path
from pprint import pprint

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

pygame.mixer.music.set_volume(60)

PathFinder = AStarFinder(diagonal_movement=DiagonalMovement.always)
grid_size = 48

phys_eps = .15

game_cycle = True

display_width, display_height = (1440, 900)
display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Dungetic')

clock = pygame.time.Clock()
directions = 'left right up down'.split()
opposites = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}

BLACK = '#000000'
WHITE = '#FFFFFF'
RED = '#FF0000'
GREEN = '#00FF00'
BLUE = '#0000FF'

# images and surfaces
map_image = pygame.image.load('../images/interfaces/old_map2.jpg').convert_alpha()
map_image = pygame.transform.scale(map_image, (
    int(map_image.get_width() / 1.5), int(map_image.get_height() * 0.8))).convert_alpha()

cursor_for_battle = pygame.image.load('../images/weapons/sword.png')
cursor_for_battle = pygame.transform.scale(cursor_for_battle,
                                           (cursor_for_battle.get_width() // 5, cursor_for_battle.get_height() // 5))
inventory_image = pygame.image.load('../images/interfaces/inventory.png').convert_alpha()

stone_floor = pygame.transform.scale(pygame.image.load('../images/surroundings/stone_floor.jpg'), (display_width, display_height))
wooden_floor = pygame.transform.scale(pygame.image.load('../images/surroundings/wooden_floor.jpg'), (display_width, display_height))

bloor = pygame.Surface((display_width, display_height))
screen_blur = pygame.Surface((display_width, display_height))
bloor.set_alpha(15)
screen_blur.set_alpha(35)
current_interface = None

# # # # # # # # fonts # # # # # # #
text_font = pygame.font.Font(None, 35)
active_font = pygame.font.Font(None, 50)
inventory_font = pygame.font.SysFont('Cambria', 75)

# borders

left_border = pygame.Rect(5, 0, 5, display_height)
right_border = pygame.Rect(display_width - 15, 0, 5, display_height)
upper_border = pygame.Rect(0, 5, display_width + 5, 5)
lower_border = pygame.Rect(0, display_height - 15, display_width, 5)
