from classes.entities import *

class Drop:

    def __init__(self, x, y, lootcls: type):
        self.loot = lootcls()
        self.x = x
        self.y = y
        self.sprite = pygame.transform.rotate(self.loot.sprite['left'], random.randint(0, 360))
        self.sprite.set_colorkey('#FFFFFF')
        self.rect = self.sprite.get_rect(topleft=(x, y))
        self.active = False
        self.picked = False

    def picked_up(self, entity: Heretic):
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

    def collide(self, entity: Heretic):
        self.active = False
        if self.rect.colliderect(entity.phys_rect):
            self.active = True
            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                if self.rect.collidepoint((x, y)):
                    entity.weapon = self.loot
                    self.picked_up(entity)
            print(self.active)
