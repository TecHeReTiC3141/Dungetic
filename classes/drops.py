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


class SellingGood(LyingItem):

    def __init__(self, x, y, lootcls: type, price):
        super().__init__(x, y, lootcls)
        self.sprite = self.loot.sprite['left'] if isinstance(self.loot.sprite, dict) else self.loot.sprite

        self.background = pygame.transform.scale(pygame.image.load('../images/surroundings/pallet.png'),
                                                 (self.rect.width, self.rect.height + 30))
        pygame.draw.rect(self.background, 'white',
                         (3, self.rect.height, self.rect.width - 6, 26))
        price_surf = text_font.render(f'{price} $', True, 'black')
        self.background.blit(price_surf, (self.background.get_width() // 2 -
                                          price_surf.get_width() // 2,
                                          self.rect.height + 2))
        self.loot.autopicked = False
        self.background.set_colorkey(BLACK)
        self.price = price

    def draw_object(self, display):
        display.blit(self.background, self.rect.topleft)
        if self.active:
            # self.background.fill(WHITE)
            display.blit(self.sprite, self.rect.move(0, -20))
        else:
            display.blit(self.sprite, self.rect)

    def picked_up(self, entity: Heretic):
        if self.price <= entity.actual_money and not self.picked:
            self.loot.picked_up(entity)
            entity.actual_money -= self.price
            self.picked = True
