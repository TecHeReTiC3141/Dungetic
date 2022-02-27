from classes.entities import *

class Wall:

    def __init__(self, x, y, width, height, collised=False, movable=False, health=120):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = height
        self.active_zone = pygame.Rect(x - 100, y, width + 51, height + 1)
        self.phys_rect = pygame.Rect(x, y, width, height)
        self.inner_phys_rect = pygame.Rect(x + 10, y + 10,
                                           max(width - 30, 10), max(height - 30, 10))
        self.visible_zone = pygame.Surface((width, height))
        self.visible_zone.set_colorkey('#FFFFFF')
        self.collised = collised
        self.health = health
        self.movable = movable

    def draw_object(self, display: pygame.Surface):
        pygame.draw.rect(self.visible_zone, (50, 50, 50), (0, 0, self.width, self.height))
        pygame.draw.rect(self.visible_zone, (WHITE),
                         (15, 15, self.inner_phys_rect.width, self.inner_phys_rect.height))
        display.blit(self.visible_zone, self.phys_rect)

    def collide(self, entities: list[Heretic]):
        for entity in entities:
            if self.phys_rect.colliderect(entity.phys_rect):
                move = [0, 0]
                if self.phys_rect.left + 10 >= entity.phys_rect.right:
                    move[0] = 1
                    entity.phys_rect.right = self.phys_rect.left + 1
                elif self.phys_rect.right - 10 <= entity.phys_rect.left:
                    move[0] = -1
                    entity.phys_rect.left = self.phys_rect.right - 1
                elif self.phys_rect.top + 10 >= entity.phys_rect.bottom:
                    move[1] = 1
                    entity.phys_rect.bottom = self.phys_rect.top + 1
                elif self.phys_rect.bottom - 10 <= entity.phys_rect.top:
                    move[1] = -1
                    entity.phys_rect.top = self.phys_rect.bottom - 1

                self.phys_rect.move_ip(*move)
                self.inner_phys_rect.move_ip(*move)

                if entity.phys_rect.colliderect(self.inner_phys_rect):
                    if entity.direction == 'up':
                        entity.phys_rect.top = self.phys_rect.bottom
                    elif entity.direction == 'down':
                        entity.phys_rect.bottom = self.phys_rect.top
                    elif entity.direction == 'left':
                        entity.phys_rect.left = self.phys_rect.right
                    else:
                        entity.phys_rect.right = self.phys_rect.left


                entity.speed = 1
            else:
                entity.speed = 5

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