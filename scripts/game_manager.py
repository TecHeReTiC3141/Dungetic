import pygame

from scripts.constants_and_sources import display_width, display_height

class GameManager:
    possible_states = ['main_menu',
                       'settings',
                       'main_game',
                       'inventory',
                       'inventory_skills',
                       'inventory_stats']

    def __init__(self, state='main_menu'):
        if state not in self.possible_states:
            raise RuntimeError('State is not supported')
        self.state = state
        self.blood = True
        self.res = (display_width, display_height)
        self.full = False

    def update(self, res: tuple, blood=True, full=False) -> pygame.Surface:
        self.res = res
        self.blood = blood
        self.full = full

        if self.full:
            return pygame.display.set_mode(self.res, pygame.FULLSCREEN)
        return pygame.display.set_mode(self.res)


