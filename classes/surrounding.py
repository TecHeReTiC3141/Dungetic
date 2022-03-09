from classes.entities import *


class Container:

    def __init__(self, content: list):
        self.content = content



class Breakable:
    def __init__(self, health):
        self.health = health
        self.is_broken = False

    def get_broken(self):
        print(f'{self} broken')
        self.is_broken = True


class Wall:

    def __init__(self, x, y, width, height, collised=False, movable=False, *args):
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
        self.movable = movable
        super().__init__(*args)

    def draw_object(self, display: pygame.Surface):

        # pygame.draw.rect(display, ('#CCCCCC'), self.outer_phys_rect)
        pygame.draw.rect(self.visible_zone, (70, 70, 70), (0, 0, self.width, self.height))

        display.blit(self.visible_zone, self.phys_rect)
        # pygame.draw.rect(display, ('#AAAAAA'), self.inner_phys_rect)

    def collide(self, entities: list[Heretic]):

        for entity in entities:

            if entity.phys_rect.collidelist([self.outer_phys_rect, self.phys_rect]) == -1:
                for direct in entity.collised_walls:
                    if entity.collised_walls[direct] == self:
                        entity.speed_directions[direct] = 5
                        entity.collised_walls[direct] = None

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


class Vase(Wall, Breakable):

    def __init__(self,  x, y, width, height, collised=False, movable=False, health=120):
        super().__init__(x, y, width, height, collised, movable, health)
        self.sprite = pygame.image.load('../images/Vase1.png').convert_alpha()
        self.sprite.set_colorkey('#FFFFFF')

    def draw_object(self, display: pygame.Surface):
        self.visible_zone.fill('#FFFFFF')
        display.blit(self.visible_zone, self.phys_rect)
        display.blit(self.sprite, self.phys_rect)
        return self.visible_zone


class Room:

    def __init__(self, obst_list: list[Wall], containers: list[Wall], entities_list: list[NPC], entrances, floor: str):
        self.obst_list = obst_list
        self.containers = containers
        self.entities_list = entities_list
        self.entrances = entrances
        self.floor = c_a_s.stone_floor if floor == 'stone' else c_a_s.wooden_floor
        self.visited = False

    def draw_object(self, display):
        display.blit(self.floor, (0, 0))
        for wall in self.obst_list + self.containers:
            wall.draw_object(display)
        for entity in self.entities_list:
            entity.draw_object(display)

    def physics(self, heretic: Heretic):
        for wall in self.obst_list + self.containers:
            wall.collide(self.entities_list + [heretic])

    def life(self):
        for entity in self.entities_list:
            entity.passive_exist()

    def clear(self):
        self.containers = list(filter(lambda i: hasattr(i, 'is_broken') and i.is_broken == False,
                                      self.containers))

