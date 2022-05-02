import pygame

from scripts.constants_and_sources import display_width, display_height

class GameManager:
    possible_states = ['main_menu',
                       'settings',
                       'main_game',
                       'inventory',
                       'inventory_skills',
                       'inventory_stats']

    def __init__(self, res: tuple, dungeon, cur_room, state='main_menu', caption='Dungetic'):

        if state not in self.possible_states:
            raise RuntimeError('State is not supported')
        self.state = state
        self.blood = True
        self.res = res
        self.full = False
        self.gamma = 1.
        self.display = pygame.display.set_mode(self.res)
        pygame.display.set_caption(caption)


        self.dungeon = dungeon
        self.curr_room = cur_room
        self.sound_vol = .5
        self.music_vol = .5

    def update(self, res: tuple, blood=True, full=False):
        self.res = res
        self.blood = blood
        self.full = full

        if self.full:
            self.display = pygame.display.set_mode(self.res, pygame.FULLSCREEN)
        else:
            self.display = pygame.display.set_mode(self.res)

