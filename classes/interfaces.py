from classes.guis import *


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

    def action(self, mouse: tuple, entity: Heretic = None, action_type: int = None):
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

    def update(self, mouse, ):
        if self.rect.collidepoint(mouse):
            pass


class ChangeState(Button):

    def __init__(self, x, y, width, height, text, color, manager: GameManager, state: str):
        super().__init__(x, y, width, height, text, color)
        self.manager = manager
        self.state = state

    def update(self, mouse: tuple):
        if self.rect.collidepoint(mouse):
            self.manager.state = self.state


class SimpleButton(Button):

    def __init__(self, x, y, width, height, text, color, action):
        super().__init__(x, y, width, height, text, color)
        self.action = action

    def update(self, mouse: tuple, ):
        if self.rect.collidepoint(mouse):
            self.action()


class CreateWindow(ChangeState):

    def __init__(self, x, y, width, height, text, color, manager: GameManager,
                 window: type, state: str = None, **kwargs):
        super().__init__(x, y, width, height, text, color, manager, state)
        self.wind = window
        self.kwargs = kwargs

    def update(self, mouse: tuple):
        if self.rect.collidepoint(mouse):
            self.wind(self.manager, **self.kwargs)


# TODO create a separate class for buttons which create gui


class InterContainer(Button):

    def __init__(self, x, y, width, height, ind=-1, active=True):
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.content = None
        self.active = active
        self.ind = ind

    def draw_object(self, display: pygame.Surface):
        self.image.fill((184, 173, 118))
        pygame.draw.rect(self.image, (0, 0, 200), (0, 0, self.rect.width,
                                                   self.rect.height), border_radius=8)
        pygame.draw.rect(self.image, (190, 190, 190), (15, 15,

                                                       self.rect.width - 30,
                                                       self.rect.height - 30))
        if isinstance(self.content, Loot):
            self.content.draw_object(self.image,
                                     self.rect.width // 6,
                                     self.rect.height // 6, in_inventory=True)
        display.blit(self.image, self.rect)

    def update(self, mouse: tuple, entity: Heretic = None, action_type: int = None):

        if isinstance(self.content, Loot) and self.active \
                and self.rect.collidepoint(mouse):
            if action_type == 1:
                return self.content

            elif action_type == 3:
                if type(self.ind) == int:
                    effect = self.content.interact(entity)
                    if self.content.deletion:
                        self.content = None
                    print(effect)
                    if effect is not None:
                        return effect
                else:
                    if isinstance(self.content, Fist):
                        return

                    self.content.deletion = False
                    entity.inventory.append(self.content)

                    self.content = None
                    if self.ind == 'weapon':
                        entity.weapon = Fist()
                    elif self.ind == 'helmet':
                        entity.head_armor = None
                    elif self.ind == 'armor':
                        entity.body_armor = None


class InventoryInter(Interface):

    def __init__(self, entity: Heretic, manager: GameManager):
        super().__init__()
        self.entity = entity
        skills = ChangeState(display_width // 4, display_height // 6, 250, 80, 'Skills',
                             GREEN, manager, 'main_game')
        stats = CreateWindow(display_width // 4, display_height // 6 + 90, 250, 80, 'Stats',
                            RED, manager, SkillsGui, 'inventory_stats', player=entity)
        self.manager = manager
        self.button_list = [skills, stats]
        self.containers = [InterContainer(i, j, 110, 110, ind=i + j * 5)
                           for j in range(320, 750, 120)
                           for i in range(50, 550, 120)]
        self.selected_item = None
        self.cur_effect = None
        self.weapon_cont = InterContainer(1015, 275, 120, 120, ind='weapon')
        self.helmet_cont = InterContainer(1135, 138, 120, 120, ind='helmet')
        self.armor_cont = InterContainer(1137, 278, 120, 120, ind='armor')

    def alt_draw_object(self, display):
        self.fill((184, 173, 118))
        self.blit(inventory_font.render('Инвентарь', True, (0, 0, 0)), (120, 10))
        self.blit(inventory_font.render('Часы: день/ночь', True, (0, 0, 0)), (800, 10))
        pygame.draw.rect(self, (0, 0, 0), (800, 150, 600, 60))
        pygame.draw.rect(self, (184, 173, 118), (1260, 155, 130, 50))
        pygame.draw.rect(self, (200, 0, 0), (810, 155, int(445 * self.entity.health // 100), 50))
        pygame.draw.rect(self, (0, 0, 200), (810, 230, 130, 130))
        pygame.draw.rect(self, (190, 190, 190), (825, 245, 100, 100))
        pygame.draw.rect(self, (0, 0, 200), (970, 230, 130, 130))
        pygame.draw.rect(self, (190, 190, 190), (985, 245, 100, 100))
        if isinstance(self.entity.weapon, Weapon):
            self.entity.weapon.draw_object(display, x=865, y=260)
            # self.blit(active_font.render(self.entity.weapon.type, True, (0, 0, 0)), (825, 365))
        else:
            pygame.draw.rect(self, (184, 173, 118), (860, 260, 20, 45))
            pygame.draw.polygon(self, (184, 173, 118), ((860, 260), (870, 252), (880, 260)))
            pygame.draw.rect(self, (184, 173, 118), (850, 300, 40, 6))
            pygame.draw.rect(self, (184, 173, 118), (864, 306, 12, 20))

        pygame.draw.rect(self, (184, 173, 118), (1000, 260, 50, 70))
        pygame.draw.lines(self, (184, 173, 118), True, ((1000, 260), (1040, 245), (1060, 270)), 8)
        pygame.draw.polygon(self, (184, 173, 118),
                            ((998, 260), (998, 285), (1025, 295), (1052, 285), (1052, 260)))

        pygame.draw.circle(self, (184, 173, 118), (1035, 289), 3)

        pygame.draw.line(self, (161, 96, 54), (700, 0), (700, 900), 100)

        pygame.draw.rect(self, (240, 240, 240), (870, 450, 500, 450))

        for i in range(510, 871, 60):
            pygame.draw.line(self, (0, 0, 0), (880, i), (1350, i), 5)

        for i in range(30, 521, 120):
            for j in range(320, 750, 120):
                pygame.draw.rect(self, (0, 0, 200), (i, j, 110, 110), border_radius=8)
                pygame.draw.rect(self, (190, 190, 190), (i + 15, j + 15, 80, 80))
        for i in range(len(self.entity.inventory)):
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

    def draw_object(self, display: pygame.Surface, ):
        self.blit(inventory_image, (0, 0))
        self.entity.draw_object(self, x=820, y=110, in_game=False)
        self.blit(inventory_font.render(f'{self.entity.money}', True, '#f8b800'),
                  (95 + 15 * len(str(self.entity.money)), 100))

        self.entity.weapon.draw_object(self, x=1040, y=310, direct='right')
        if isinstance(self.entity.head_armor, Helmet):
            self.entity.head_armor.draw_object(self, x=1145, y=185, direct='right')

        if isinstance(self.cur_effect, Banner):
            print(self.cur_effect.surf)
            self.cur_effect.draw_object(self)
            if self.cur_effect.life_time <= 0:
                self.cur_effect = None

        for button in self.button_list:
            button.draw_object(self)

        for container in self.containers:
            container.draw_object(self)

        self.armor_cont.draw_object(self)
        self.weapon_cont.draw_object(self)
        self.helmet_cont.draw_object(self)

        if isinstance(self.selected_item, Loot):
            self.selected_item.draw_object(self, x=785, y=430)
            for line in range(len(self.selected_item.descr)):
                self.blit(active_font.render(self.selected_item.descr[line],
                                             True, BLACK), (890, 470 + line * 50))

        display.blit(self, (0, 0))

    def open(self):
        self.selected_item = None
        for i in range(len(self.containers)):
            self.containers[i].content = None
        for i in range(len(self.entity.inventory)):
            self.containers[i].content = self.entity.inventory[i]

        self.weapon_cont.content = self.entity.weapon
        self.helmet_cont.content = self.entity.head_armor
        self.armor_cont.content = self.entity.body_armor

    def process(self, action_type, mouse):
        for container in self.containers + \
                         [self.armor_cont, self.weapon_cont, self.helmet_cont]:
            if action_type == 1:
                self.selected_item = container.update(tuple(mouse), self.entity, action_type)
            elif action_type == 3:
                self.cur_effect = container.update(tuple(mouse), self.entity, action_type)
                if self.cur_effect:
                    text, color = self.cur_effect

                    self.cur_effect = Banner(810, 280, text, 150, color)
                    print(type(self.cur_effect))

            if self.selected_item is not None:
                break

        filled = [i for i in range(len(self.containers))
                  if isinstance(self.containers[i].content, Loot)
                  and not self.containers[i].content.deletion]
        if filled:
            ma_filled = max(filled)
            for i, el in enumerate(self.entity.inventory[ma_filled + 1:], start=ma_filled + 1):
                if isinstance(el, Loot) and not el.deletion:
                    self.containers[i].content = el

        for i in range(len(self.entity.inventory)):
            if self.containers[i].content is None or \
                    isinstance(self.containers[i], Loot) \
                    and self.containers[i].content.deletion:
                self.entity.inventory[i] = None

        for button in self.button_list:
            button.update(mouse)

        # TODO add functionality of buttons in the inventory

    def close(self):
        self.entity.inventory = list(filter(lambda i: i is not None,
                                            self.entity.inventory))


class MapInter(Interface):

    def __init__(self, rooms: dict, game_manager: GameManager):
        super().__init__()
        self.manager = game_manager
        self.rooms = rooms

    def draw_object(self, display):
        display.blit(bloor, (0, 0))
        display.blit(map_image, (40, 50))
        for i in range(1, dung_width + 1):
            for j in range(1, dung_length + 1):
                cur_ind = i * dung_length + j
                room_x = 10 + j * 80
                room_y = 10 + i * 80
                if self.rooms.get(cur_ind) is not None and self.rooms[cur_ind].visited:
                    if self.rooms[cur_ind].type == 'common':
                        pygame.draw.rect(display, (240, 240, 240), (room_x, room_y, 45, 35))
                    elif self.rooms[cur_ind].type == 'storage':
                        pygame.draw.rect(display, '#8d6712', (room_x, room_y, 45, 35))
                    if 'up' in self.rooms[cur_ind].entrances:
                        pygame.draw.rect(display, (200, 200, 200), (room_x + 12, room_y - 25, 20, 25))
                    if 'down' in self.rooms[cur_ind].entrances:
                        pygame.draw.rect(display, (200, 200, 200), (room_x + 12, room_y + 35, 20, 20))
                    if 'right' in self.rooms[cur_ind].entrances:
                        pygame.draw.rect(display, (200, 200, 200), (room_x + 45, room_y + 7, 20, 20))
                    if 'left' in self.rooms[cur_ind].entrances:
                        pygame.draw.rect(display, (200, 200, 200), (room_x - 15, room_y + 7, 15, 20))
                    if cur_ind == self.manager.curr_room:
                        pygame.draw.rect(display, BLACK, (room_x + 5, room_y + 7, 15, 20))


class MainMenu(Interface):

    def __init__(self, manager: GameManager):
        super().__init__()
        self.manager = manager
        play = ChangeState(display_width // 3, display_height // 2, 250, 80, 'Start',
                           GREEN, manager, 'main_game')
        settings = CreateWindow(display_width // 3, display_height // 2 + 100, 250, 80, 'Settings',
                               BLUE, manager, Settings)
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
