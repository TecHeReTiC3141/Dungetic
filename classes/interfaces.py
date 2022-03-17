import scripts.constants_and_sources as c_a_s
from classes.Heretic import Heretic
from scripts.constants_and_sources import *
from scripts.game_manager import GameManager


class Interface(pygame.Surface):
    '''
    Interface for all custom surfaces used in Dungetic
    '''

    def __init__(self):
        super().__init__((display_width, display_height))

    def draw_object(self, display: pygame.Surface, ):
        display.blit(self, (0, 0))

    def process(self, *args):
        pass


class UI:

    def action(self, mouse: tuple):
        pass


button_font = pygame.font.SysFont('Ubuntu', 45)


class Button(UI):

    def __init__(self, x, y, width, height, text, color):
        self.image = pygame.Surface((width, height))
        self.image.set_colorkey(BLACK)

        self.x, self.y = x, y
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.label = button_font.render(text, True, '#010101')

    def draw_object(self, display: pygame.Surface):
        pygame.draw.rect(self.image, pygame.Color('Grey'), (0, 0, self.rect.width, self.rect.height), border_radius=15)
        pygame.draw.rect(self.image, self.color,
                         (0, 0, self.rect.width, self.rect.height - 5), border_radius=15)

        self.image.blit(self.label, (self.rect.width // 3, self.rect.height // 5))
        display.blit(self.image, self.rect)

    def update(self, mouse,):
        if self.rect.collidepoint(mouse):
            pass


class ChangeState(Button):
    def __init__(self, x, y, width, height, text, color, manager: GameManager, state: str):
        super().__init__(x, y, width, height, text, color)
        self.manager = manager
        self.state = state

    def update(self, mouse):
        if self.rect.collidepoint(mouse):
            self.manager.state = self.state


class SimpleButton(Button):
    def __init__(self, x, y, width, height, text, color, action):
        super().__init__(x, y, width, height, text, color)
        self.action = action

    def update(self, mouse,):
        if self.rect.collidepoint(mouse):
            self.action()

class Switcher(UI):

    def __init__(self, x, y, text, state, atr: str):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 80, 45)
        self.label = button_font.render(text, True, BLACK)
        self.images = {True: '', False: ''}




class Inventory(Interface):

    def draw_object(self, display, heretic: Heretic):
        self.fill((184, 173, 118))
        self.blit(inventory_font.render('Инвентарь', True, (0, 0, 0)), (120, 10))
        self.blit(inventory_font.render('Часы: день/ночь', True, (0, 0, 0)), (800, 10))
        pygame.draw.rect(self, (0, 0, 0), (800, 150, 600, 60))
        pygame.draw.rect(self, (184, 173, 118), (1260, 155, 130, 50))
        pygame.draw.rect(self, (200, 0, 0), (810, 155, int(445 * heretic.health // 100), 50))
        pygame.draw.rect(self, (0, 0, 200), (810, 230, 130, 130))
        pygame.draw.rect(self, (190, 190, 190), (825, 245, 100, 100))
        pygame.draw.rect(self, (0, 0, 200), (970, 230, 130, 130))
        pygame.draw.rect(self, (190, 190, 190), (985, 245, 100, 100))
        if heretic.weapon != 'none':
            heretic.weapon.draw_object(865, 260)
            self.blit(active_font.render(heretic.weapon.type, True, (0, 0, 0)), (825, 365))
        else:
            pygame.draw.rect(self, (184, 173, 118), (860, 260, 20, 45))
            pygame.draw.polygon(self, (184, 173, 118), ((860, 260), (870, 252), (880, 260)))
            pygame.draw.rect(self, (184, 173, 118), (850, 300, 40, 6))
            pygame.draw.rect(self, (184, 173, 118), (864, 306, 12, 20))

        if heretic.backpack:
            heretic.backpack.draw_object(1000, 260)
            self.blit(active_font.render(heretic.backpack.type, True, (0, 0, 0)), (960, 365))
        else:
            pygame.draw.rect(self, (184, 173, 118), (1000, 260, 50, 70))
            pygame.draw.lines(self, (184, 173, 118), True, ((1000, 260), (1040, 245), (1060, 270)), 8)
            pygame.draw.polygon(self, (184, 173, 118),
                                ((998, 260), (998, 285), (1025, 295), (1052, 285), (1052, 260)))

            pygame.draw.circle(self, (184, 173, 118), (1035, 289), 3)

        pygame.draw.line(self, (161, 96, 54), (700, 0), (700, 900), 100)

        pygame.draw.rect(self, (240, 240, 240), (870, 450, 500, 450))

        for i in range(510, 871, 60):
            pygame.draw.line(self, (0, 0, 0), (880, i), (1350, i), 5)

        for i in range(50, 601, 150):
            for j in range(100, 801, 150):
                pygame.draw.rect(self, (0, 0, 200), (i, j, 130, 130))
                pygame.draw.rect(self, (190, 190, 190), (i + 15, j + 15, 100, 100))
        for i in range(len(heretic.inventory)):
            pass
        # if 100 < pos[0] < 650 and pos[1] > 100:
        #     pos_index = (pos[0] - 50) // 150 + (pos[1] - 100) // 150 * 4
        #     if pos_index < len(heretic.inventory):
        #         display.blit(inventory_font.render(heretic.inventory[pos_index].type, True,
        #                                            (0, 0, 0)), (pos[0] - 100, pos[1] - 75))
        # if isinstance(chosen_item, Drop) or isinstance(chosen_item, Berry) or isinstance(chosen_item, Weapon):
        #     for i in range(len(chosen_item.description)):
        #         display.blit(active_font.render(chosen_item.description[i], True, (0, 0, 0)), (880, 465 + i * 60))
        super().draw_object(display)


class MapInter(Interface):

    def __init__(self, rooms: dict):
        super().__init__()
        self.rooms = rooms

    def draw_object(self, display):
        display.blit(bloor, (0, 0))
        display.blit(map_image, (40, 50))
        for j in range(90, 90 + dung_width * 80, 80):
            for i in range(90, 90 + dung_length * 80, 80):
                r_ind = (i - 90) // 80 + (j - 90) // 80 * dung_length + 1
                if rooms[r_ind].visited:
                    pygame.draw.rect(display, (240, 240, 240), (i, j, 45, 35))
                    if 'up' in rooms[r_ind].entrances:
                        pygame.draw.rect(display, (200, 200, 200), (i + 12, j - 25, 20, 25))
                    if 'down' in rooms[r_ind].entrances:
                        pygame.draw.rect(display, (200, 200, 200), (i + 12, j + 35, 20, 20))
                    if 'right' in rooms[r_ind].entrances:
                        pygame.draw.rect(display, (200, 200, 200), (i + 45, j + 7, 20, 20))
                    if 'left' in rooms[r_ind].entrances:
                        pygame.draw.rect(display, (200, 200, 200), (i - 15, j + 7, 15, 20))
                    if r_ind == c_a_s.curr_room:
                        pygame.draw.rect(display, BLACK, (i + 5, j + 7, 15, 20))
                else:
                    pygame.draw.rect(display, (10, 10, 10), (i, j, 45, 35))


class MainMenu(Interface):

    def __init__(self, manager: GameManager):
        super().__init__()
        self.manager = manager
        play = ChangeState(display_width // 3, display_height // 2, 250, 80, 'Start',
                      GREEN, manager, 'main_game')
        settings = ChangeState(display_width // 3, display_height // 2 + 100, 250, 80, 'Settings',
                      BLUE, manager, 'settings')
        ex = SimpleButton(display_width // 3, display_height // 2 + 200, 250, 80, 'Exit',
                      RED, exit)
        self.button_list = [play, settings, ex]

    def draw_object(self, display: pygame.Surface, ):
        self.blit(stone_floor, (0, 0))
        mainmenu_font = pygame.font.SysFont('Cambria', 75)
        main_menu = mainmenu_font.render('Welcome to Dungetic', True, BLACK)
        self.blit(main_menu, (display_width // 5, display_height // 6))
        for button in self.button_list:
            button.draw_object(self)
        display.blit(self, (0, 0))

    def process(self, mouse: tuple):
        for button in self.button_list:
            button.update(mouse, )
