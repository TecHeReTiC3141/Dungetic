import pygame

class Wall:

    def __init__(self, x, y, width, height, collised=False, movable=False, health=120):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = height
        self.active_zone = pygame.Rect(x - 100, self.y, self.width + 51, height + 1)
        self.phys_rect = pygame.Rect(x, y, width, height)
        self.visible_zone = pygame.Surface((width, height))
        self.collised = collised
        self.health = health
        self.movable = movable

    def draw_object(self, display: pygame.Surface):
        pygame.draw.rect(self.visible_zone, (50, 50, 50), self.phys_rect)
        display.blit(self.visible_zone, self.phys_rect)


class Vase(Wall):

    def draw_object(self, display):
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