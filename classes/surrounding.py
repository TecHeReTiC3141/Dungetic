import pygame

class Wall:

    def __init__(self, w_x, w_y, width, height, collised=False, movable=False, health=120):
        self.x = w_x
        self.y = w_y
        self.width = width
        self.height = height
        self.health = height
        self.active_zone = [list(range(self.x - 100, self.x + self.width + 51)),
                            list(range(self.y, self.y + self.height + 1))]
        self.visible_zone = [list(range(self.x, self.x + self.width + 1)),
                             list(range(self.y, self.y + self.height + 1))]
        self.collised = collised
        self.health = health
        self.movable = movable

    def draw_object(self, display):
        pygame.draw.rect(display, (50, 50, 50), (obj_x, obj_y, self.width, self.height))


class Vase(Wall):

    def draw_object(self, obj_x, obj_y):
        pygame.draw.polygon(display, (184, 133, 71),
                            ((obj_x, obj_y), (obj_x + 40, obj_y), (obj_x + 30, obj_y + 20), (obj_x + 10, obj_y + 20)))
        pygame.draw.polygon(display, (184, 133, 71), (
            (obj_x + 5, obj_y + 20), (obj_x + 35, obj_y + 20), (obj_x + 30, obj_y + 45), (obj_x + 10, obj_y + 45)))
        pygame.draw.polygon(display, (0, 0, 0), (
            (obj_x + 7, obj_y + 27), (obj_x + 33, obj_y + 27), (obj_x + 31, obj_y + 42), (obj_x + 9, obj_y + 42)))


class Room:
    visited = False

    def __init__(self, walls_list, entities_list, entrances, floor):
        self.walls_list = walls_list
        self.entities_list = entities_list
        self.entrances = entrances
        self.floor = floor