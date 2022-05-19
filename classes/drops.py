from classes.entities import *

class Drop:

    def __init__(self, x, y, lootcls: type):
        self.loot = lootcls()
        self.x = x
        self.y = y
        self.sprite = pygame.transform.rotate(self.loot.sprite['left']
                                              if isinstance(self.loot.sprite, dict) else self.loot.sprite,
                                              randint(0, 360))
        self.sprite.set_colorkey('#FFFFFF')
        self.rect = self.sprite.get_rect(topleft=(x, y))
        self.active = False
        self.picked = False
        self.autopicked = isinstance(self.loot, Money)

    def draw_object(self, display):
        pass

    def picked_up(self, entity: Heretic):
        if not self.picked:
            self.loot.picked_up(entity)
        self.picked = True



class LyingItem(Drop):

    def __init__(self, x, y, lootcls: type):
        super().__init__(x, y, lootcls)
        self.background = pygame.Surface((self.rect.width, self.rect.width))
        self.background.set_colorkey(BLACK)
        self.background.set_alpha(128)


    def draw_object(self, display):
        self.background.fill(BLACK)
        if self.active:
            # self.background.fill(WHITE)
            pygame.draw.circle(self.background, '#0d91b6',
                           self.background.get_rect().center, self.rect.width // 2)

        display.blit(self.sprite, self.rect)
        display.blit(self.background, self.rect.topleft)

    def collide(self, entities: list[Heretic]):
        self.active = False
        for entity in entities:
            if self.rect.colliderect(entity.cur_rect):
                self.active = True
                if self.autopicked:
                    self.picked_up(entity)
                elif pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()
                    if self.rect.collidepoint((x, y)):
                        self.picked_up(entity)
