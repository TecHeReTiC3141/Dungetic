from classes.entities import *

class Wall:

    def __init__(self, x, y, width, height, collised=False, movable=False, health=120):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = height
        self.weight = width * height // 2500
        self.active_zone = pygame.Rect(x - 100, y, width + 51, height + 1)
        self.phys_rect = pygame.Rect(x, y, width, height)
        self.inner_phys_rect = pygame.Rect(x + 10, y + 10,
                                           max(width - 20, 10), max(height - 20, 10))
        self.outer_phys_rect = pygame.Rect(x - 8, y - 8, width + 16, height + 16)
        self.visible_zone = pygame.Surface((width, height))
        self.visible_zone.set_colorkey('#FFFFFF')
        self.collised = collised
        self.health = health
        self.movable = movable

    def draw_object(self, display: pygame.Surface):

        pygame.draw.rect(display, ('#CCCCCC'), self.outer_phys_rect)
        pygame.draw.rect(display, (50, 50, 50), self.phys_rect)

        display.blit(self.visible_zone, self.phys_rect)
        pygame.draw.rect(display, ('#AAAAAA'), self.inner_phys_rect)

    def collide(self, entities: list[Heretic]):
        for entity in entities:

            if entity.phys_rect.collidelist([self.outer_phys_rect, self.phys_rect]) != -1:
                entity.speed = max(1, entity.speed - self.weight)
                entity.colliding = self
            elif entity.colliding is None or entity.colliding == self:
                entity.speed = 5
            if self.phys_rect.colliderect(entity.phys_rect):

                move = [0, 0]
                if self.phys_rect.left + 10 >= entity.phys_rect.right:
                    move[0] = 1

                if self.phys_rect.right - 10 <= entity.phys_rect.left:
                    move[0] = -1
                if self.phys_rect.top + 10 >= entity.phys_rect.bottom:
                    move[1] = 1

                if self.phys_rect.bottom - 10 <= entity.phys_rect.top:
                    move[1] = -1
                print(self, move)
                self.phys_rect.move_ip(*move)
                self.inner_phys_rect.move_ip(*move)
                self.outer_phys_rect.move_ip(*move)

                # if entity.phys_rect.colliderect(self.inner_phys_rect):
                #     if entity.phys_rect.collidepoint(self.inner_phys_rect.midtop):
                #         entity.phys_rect.bottom = self.phys_rect.top
                #     elif entity.phys_rect.collidepoint(self.inner_phys_rect.midright):
                #         entity.phys_rect.left = self.phys_rect.right
                #     elif entity.phys_rect.collidepoint(self.inner_phys_rect.midleft):
                #         entity.phys_rect.right = self.phys_rect.left
                #     elif entity.phys_rect.collidepoint(self.inner_phys_rect.midbottom):
                #         entity.phys_rect.top = self.phys_rect.bottom
                #
                #     else:
                #         if entity.direction == 'up':
                #             entity.phys_rect.top = self.phys_rect.bottom
                #         elif entity.direction == 'down':
                #             entity.phys_rect.bottom = self.phys_rect.top
                #         elif entity.direction == 'left':
                #             entity.phys_rect.right = self.phys_rect.left
                #         else:
                #             entity.phys_rect.left = self.phys_rect.right



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

    def __init__(self, walls_list: list[Wall], entities_list: list[NPC], entrances, floor: str):
        self.walls_list = walls_list
        self.entities_list = entities_list
        self.entrances = entrances
        self.floor = stone_floor if floor == 'stone' else wooden_floor

    def draw_object(self, display):
        display.blit(self.floor, (0, 0))
        for wall in self.walls_list:
            wall.draw_object(display)
        for entity in self.entities_list:
            entity.draw_object(display)

    def physics(self, heretic: Heretic):
        for wall in self.walls_list:
            wall.collide(self.entities_list + [heretic])

    def life(self):
        for entity in self.entities_list:
            entity.passive_exist()