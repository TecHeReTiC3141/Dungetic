from entities import *

class Wall:

    def __init__(self, x, y, width, height, collised=False, movable=False, health=120):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = height
        self.active_zone = pygame.Rect(x - 100, y, width + 51, height + 1)
        self.phys_rect = pygame.Rect(x, y, width, height)
        self.visible_zone = pygame.Surface((width, height))
        self.visible_zone.set_colorkey('#FFFFFF')
        self.collised = collised
        self.health = health
        self.movable = movable

    def draw_object(self, display: pygame.Surface):
        pygame.draw.rect(self.visible_zone, (50, 50, 50), self.phys_rect)
        display.blit(self.visible_zone, self.phys_rect)

    def collide(self):
        pass

class Vase(Wall):

    def draw_object(self, display: pygame.Surface):
        self.visible_zone.fill('#FFFFFF')
        pygame.draw.polygon(display, (184, 133, 71),
                            ((0, 0), (0 + 40, 0), (0 + 30, 0 + 20), (0 + 10, 0 + 20)))
        pygame.draw.polygon(self.visible_zone, (184, 133, 71), (
            (0 + 5, 0 + 20), (0 + 35, 0 + 20),
            (0 + 30, 0 + 45), (0 + 10, 0 + 45)))
        pygame.draw.polygon(self.visible_zone, (1, 1, 1), (
            (0 + 7, 0 + 27), (0 + 33, 0 + 27),
            (0 + 31, 0 + 42), (0 + 9, 0 + 42)))

        display.blit(self.visible_zone, self.phys_rect)
        return self.visible_zone

class Room:
    visited = False

    def __init__(self, walls_list, entities_list, entrances, floor):
        self.walls_list = walls_list
        self.entities_list = entities_list
        self.entrances = entrances
        self.floor = stone_floor if floor == 'stone' else wooden_floor

    def draw_object(self, display):
        display.blit(self.floor, (0, 0))