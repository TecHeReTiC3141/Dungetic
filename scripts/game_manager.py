import pygame

from scripts.constants import display_width, display_height, stone_floor

class GameManager:
    possible_states = ['main_menu',
                       'settings',
                       'main_game',
                       'inventory',
                       'inventory_skills',
                       'inventory_stats']

    def __init__(self, res: tuple, dungeon: dict, cur_room,
                 state='main_menu', caption='Dungetic'):

        if state not in self.possible_states:
            raise RuntimeError('State is not supported')
        self.state = state
        self.blood = True
        self.show_damage = False
        self.res = res
        self.full = False
        self.gamma = 1.
        self.display = pygame.display.set_mode(res)
        self.display.blit(stone_floor, (0, 0))

        pygame.display.set_caption(caption)

        self.is_paused = False
        self.dungeon = dungeon
        self.curr_room = cur_room
        self.surf = pygame.Surface((self.dungeon[cur_room].width,
                                                       self.dungeon[cur_room].height))
        self.sound_vol = .5
        self.music_vol = .5

    def update(self, res: tuple, blood=True, full=False, show_dam=False):
        self.res = res
        self.blood = blood
        self.full = full
        self.show_damage = show_dam

        if self.full:
            self.display = pygame.display.set_mode(self.res, pygame.FULLSCREEN)
        else:
            self.display = pygame.display.set_mode(self.res)

    def set_room(self, cur_room):
        self.curr_room = cur_room
        self.surf = pygame.transform.scale(self.surf, (self.dungeon[cur_room].width,
                                                       self.dungeon[cur_room].height))
