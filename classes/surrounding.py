from math import *

import pygame

from classes.drops import *
from classes.decors import *


class Container:
    # interface for all game containers

    def __init__(self, content: list):
        self.content = content


class Breakable:
    def __init__(self, health, *args):
        self.health = health
        self.is_broken = False
        super().__init__(*args)

    def get_broken(self):
        self.is_broken = True
        if isinstance(self, Container):
            return self.content


class Wall:

    def __init__(self, x, y, width, height, collised=False, movable=False, *args):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = height
        self.weight = width * height // 2500
        self.active_zone = pygame.Rect(x - 100, y, width + 51, height + 1)
        self.cur_rect = pygame.Rect(x, y, width, height)
        self.prev_rect = self.cur_rect.copy()
        self.inner_phys_rect = pygame.Rect(x + 5, y + 5,
                                           max(width - 10, 10), max(height - 10, 10))
        self.outer_phys_rect = pygame.Rect(x - 10, y - 10, width + 20, height + 20)
        self.visible_zone = pygame.Surface((width, height))
        self.sprite = pygame.Surface((width, height))
        self.mask = pygame.mask.from_surface(self.sprite)
        self.visible_zone.set_colorkey('Black')
        self.sprite.set_colorkey('Black')
        pygame.draw.rect(self.sprite, (70, 70, 70), (0, 0, self.width, self.height), border_radius=8)


        self.collised = collised
        self.movable = movable
        super().__init__(*args)

    def draw_object(self, display: pygame.Surface):

        # pygame.draw.rect(display, ('#CCCCCC'), self.outer_phys_rect)
        pygame.draw.rect(self.sprite, (70, 70, 70), (0, 0, self.width, self.height), border_radius=8)

        display.blit(self.sprite, self.cur_rect)
        # pygame.draw.rect(display, ('#AAAAAA'), self.inner_phys_rect)

    def collide(self, entities: list[Heretic], direction: str, walls_list: list):

        for entity in entities:
            if isinstance(entity, NPC):
                if entity.cur_rect.collidelist([self.outer_phys_rect, self.cur_rect]) == -1:
                    for direct in entity.collised_walls:
                        if entity.collised_walls[direct] == self:
                            entity.speed_directions[direct] = 5
                            entity.collised_walls[direct] = None
                move = [0, 0]
                if self.cur_rect.colliderect(entity.cur_rect):

                    if self.cur_rect.left + 15 >= entity.cur_rect.right:
                        move[0] = max(5 - self.weight, 1)
                        entity.collised_walls['right'] = self
                        if not self.movable:
                            entity.speed_directions['right'] = 0
                        else:
                            entity.speed_directions['right'] = max(5 - self.weight, 1)

                    if self.cur_rect.right - 15 <= entity.cur_rect.left:
                        move[0] = -max(5 - self.weight, 1)
                        entity.collised_walls['left'] = self
                        if not self.movable:
                            entity.speed_directions['left'] = 0
                        else:
                            entity.speed_directions['left'] = max(5 - self.weight, 1)
                    if self.cur_rect.top + 15 >= entity.cur_rect.bottom:
                        move[1] = max(5 - self.weight, 1)
                        entity.collised_walls['down'] = self
                        if not self.movable:
                            entity.speed_directions['down'] = 0
                        else:
                            entity.speed_directions['down'] = max(5 - self.weight, 1)

                    if self.cur_rect.bottom - 15 <= entity.cur_rect.top:
                        move[1] = -max(5 - self.weight, 1)
                        entity.collised_walls['up'] = self
                        if not self.movable:
                            entity.speed_directions['up'] = 0
                        else:
                            entity.speed_directions['up'] = max(5 - self.weight, 1)
            else:
                move = [0, 0]
                if entity.cur_rect.colliderect(self.cur_rect):
                    if direction == 'hor':
                        # left side
                        if entity.cur_rect.right >= self.cur_rect.left >= entity.prev_rect.right:
                            entity.cur_rect.right = self.cur_rect.left
                            move[0] = max(5 - self.weight, 1)
                        # right side
                        elif entity.cur_rect.left <= self.cur_rect.right <= entity.prev_rect.left:
                            entity.cur_rect.left = self.cur_rect.right
                            move[0] = -max(5 - self.weight, 1)
                    else:
                        # top side
                        if entity.cur_rect.bottom >= self.cur_rect.top >= entity.prev_rect.bottom:
                            entity.cur_rect.bottom = self.cur_rect.top
                            move[1] = max(5 - self.weight, 1)
                        # bottom side
                        elif entity.cur_rect.top <= self.cur_rect.bottom <= entity.prev_rect.top:
                            entity.cur_rect.top = self.cur_rect.bottom
                            move[1] = -max(5 - self.weight, 1)

            # TODO update physics for all entities
            if self.movable:
                self.prev_rect = self.cur_rect.copy()

                self.cur_rect.move_ip(*move)
                self.inner_phys_rect.move_ip(*move)
                self.outer_phys_rect.move_ip(*move)
                for wall in walls_list:
                    if self.cur_rect.colliderect(wall.cur_rect):
                        if direction == 'hor':
                            # left side
                            if self.cur_rect.right >= wall.cur_rect.left >= self.prev_rect.right:
                                if not wall.movable:
                                    self.cur_rect.right = wall.cur_rect.left
                                else:
                                    wall.cur_rect.left = self.cur_rect.right

                            # right side
                            elif self.cur_rect.left <= wall.cur_rect.right <= self.prev_rect.left:
                                if not wall.movable:
                                    self.cur_rect.left = wall.cur_rect.right
                                else:
                                    wall.cur_rect.right = self.cur_rect.left

                        else:
                            # top side
                            if self.cur_rect.bottom >= wall.cur_rect.top >= self.prev_rect.bottom:
                                if not wall.movable:
                                    self.cur_rect.bottom = wall.cur_rect.top
                                else:
                                    wall.cur_rect.top = self.cur_rect.bottom

                            # bottom side
                            elif self.cur_rect.top <= wall.cur_rect.bottom <= self.prev_rect.top:
                                if not wall.movable:
                                    self.cur_rect.top = wall.cur_rect.bottom
                                else:
                                    wall.cur_rect.bottom = self.cur_rect.top


    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop('visible_zone')
        state.pop('sprite')
        state.pop('mask')
        return state

    def __setstate__(self, state):
        width, height = state['width'], state['height']
        self.visible_zone = pygame.Surface((width, height))
        self.sprite = pygame.Surface((width, height))
        self.visible_zone.set_colorkey('Black')
        self.sprite.set_colorkey('Black')
        self.mask = pygame.mask.from_surface(self.sprite)
        self.__dict__.update(state)


class Vase(Wall, Breakable, Container):

    sprite_path = '../images/surroundings/Vase1.png'

    def __init__(self, x, y, width, height, collised=False, movable=False, health=120, container=None):
        super().__init__(x, y, width, height, collised, movable, health, container)

        self.sprite = pygame.image.load(self.sprite_path).convert_alpha()
        self.visible_zone = pygame.Surface(self.sprite.get_size())
        self.sprite.set_colorkey('#FFFFFF')
        self.visible_zone.set_colorkey('White')
        self.mask = pygame.mask.from_surface(self.sprite)
        self.cur_rect.update(*self.cur_rect.topleft, *self.sprite.get_size())

    def draw_object(self, display: pygame.Surface):
        self.visible_zone.fill('#FFFFFF')
        self.visible_zone.blit(self.sprite, (0, 0))
        display.blit(self.visible_zone, self.cur_rect)
        return self.visible_zone

    def __setstate__(self, state):
        self.sprite = pygame.image.load(self.sprite_path).convert_alpha()
        self.visible_zone = pygame.Surface(self.sprite.get_size())
        self.sprite.set_colorkey('#FFFFFF')
        self.visible_zone.set_colorkey('White')
        self.mask = pygame.mask.from_surface(self.sprite)
        self.__dict__.update(state)


class Crate(Vase):

    sprite_path = '../images/surroundings/crate.png'

    def __init__(self, x, y, width, height, collised=False,
                 movable=False, health=120, container=None):
        super().__init__(x, y, width, height, collised,
                         movable, health, container)
        self.sprite = pygame.transform.scale(pygame.image.load(self.sprite_path), (width, height))
        self.visible_zone = pygame.Surface(self.sprite.get_size())
        self.visible_zone.set_colorkey('White')
        self.cur_rect.update(*self.cur_rect.topleft, width, height)


class TrapDoor:

    def __init__(self, x, y, width=200, height=200):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.active = False
        self.active_zone = pygame.Rect(x - width // 2, y - height // 2,
                                       width * 3 // 2, height)
        self.rect = pygame.Rect(x, y, width, height // 2)

    def collide(self, player: Heretic):
        if self.rect.colliderect(player.cur_rect):
            return True
        elif self.active_zone.colliderect(player.cur_rect):
            self.active = True
        else:
            self.active = False
        return False

    def draw_object(self, display: pygame.Surface):
        pygame.draw.rect(display, 'black' if not self.active else 'blue', self.rect)


class MyNode:

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.status = 1

    def collide(self, obsts: list[Wall]):
        for wall in obsts:
            if wall.outer_phys_rect.colliderect(self.rect):
                self.status = 0
                break
        else:
            self.status = 1

    def draw_object(self, display):
        pygame.draw.rect(display, [RED, BLUE][self.status], self.rect)

        # drawing the grid
        pygame.draw.line(display, BLACK, self.rect.topleft, (display_width, self.rect.top))
        pygame.draw.line(display, BLACK, self.rect.bottomleft, (display_width, self.rect.bottom))
        pygame.draw.line(display, BLACK, self.rect.topleft, (self.rect.left, display_height))
        pygame.draw.line(display, BLACK, self.rect.topright, (self.rect.right, display_height))
