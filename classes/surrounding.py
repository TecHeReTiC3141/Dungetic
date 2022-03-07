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
        self.inner_phys_rect = pygame.Rect(x + 5, y + 5,
                                           max(width - 10, 10), max(height - 10, 10))
        self.outer_phys_rect = pygame.Rect(x - 5, y - 5, width + 10, height + 10)
        self.visible_zone = pygame.Surface((width, height))
        self.visible_zone.set_colorkey('#FFFFFF')
        self.collised = collised
        self.health = health
        self.movable = movable

    def draw_object(self, display: pygame.Surface):

        # pygame.draw.rect(display, ('#CCCCCC'), self.outer_phys_rect)
        pygame.draw.rect(self.visible_zone, (70, 70, 70), (0, 0, self.width, self.height))

        display.blit(self.visible_zone, self.phys_rect)
        # pygame.draw.rect(display, ('#AAAAAA'), self.inner_phys_rect)

    def collide(self, entities: list[Heretic]):

        for entity in entities:

            if entity.phys_rect.collidelist([self.outer_phys_rect, self.phys_rect]) == -1:
                for dir in entity.collised_walls:
                    if entity.collised_walls[dir] == self:
                        entity.speed_directions[dir] = 5
                        entity.collised_walls[dir] = None

            if self.phys_rect.colliderect(entity.phys_rect):
                move = [0, 0]
                if self.phys_rect.left + 15 >= entity.phys_rect.right:
                    move[0] = max(5 - self.weight, 1)
                    entity.collised_walls['right'] = self
                    if not self.movable:

                        entity.speed_directions['right'] = 0
                    else:
                        entity.speed_directions['right'] = max(5 - self.weight, 1)

                if self.phys_rect.right - 15 <= entity.phys_rect.left:
                    move[0] = -max(5 - self.weight, 1)
                    entity.collised_walls['left'] = self
                    if not self.movable:

                        entity.speed_directions['left'] = 0
                    else:
                        entity.speed_directions['left'] = max(5 - self.weight, 1)
                if self.phys_rect.top + 15 >= entity.phys_rect.bottom:
                    move[1] = max(5 - self.weight, 1)
                    entity.collised_walls['down'] = self
                    if not self.movable:

                        entity.speed_directions['down'] = 0
                    else:
                        entity.speed_directions['down'] = max(5 - self.weight, 1)

                if self.phys_rect.bottom - 15 <= entity.phys_rect.top:
                    move[1] = -max(5 - self.weight, 1)
                    entity.collised_walls['up'] = self
                    if not self.movable:

                        entity.speed_directions['up'] = 0
                    else:
                        entity.speed_directions['up'] = max(5 - self.weight, 1)

                if self.movable:
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
        self.floor = c_a_s.stone_floor if floor == 'stone' else c_a_s.wooden_floor

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