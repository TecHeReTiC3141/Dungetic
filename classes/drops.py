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

    def draw_object(self, display):
        pass

    def picked_up(self, entity: Heretic):
        if not self.picked:
            self.loot.picked_up(entity)
        self.picked = True

    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop('sprite')

        return state

    def __setstate__(self, state):
        self.sprite = pygame.transform.rotate(state['loot'].sprite['left']
                                              if isinstance(self.loot.sprite, dict) else state['loot'].sprite,
                                              randint(0, 360))
        self.__dict__.update(state)


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

    def collide(self, entities: list[Heretic], mouse: tuple = None):
        self.active = False
        for entity in entities:
            if self.rect.colliderect(entity.cur_rect):
                self.active = True
                if self.loot.autopicked:
                    self.picked_up(entity)
                elif mouse:
                    if self.rect.collidepoint(mouse):
                        self.picked_up(entity)

    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop('sprite')
        state.pop('background')
        return state

    def __setstate__(self, state):
        self.sprite = pygame.transform.rotate(state['loot'].sprite['left']
                                              if isinstance(state['loot'].sprite, dict) else state['loot'].sprite,
                                              randint(0, 360))
        self.background = pygame.Surface((state['rect'].width, state['rect'].width))
        self.background.set_colorkey(BLACK)
        self.background.set_alpha(128)
        self.__dict__.update(state)