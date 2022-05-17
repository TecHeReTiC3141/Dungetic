from classes.surrounding import *
from scripts.algorithms_of_generation import generate_dungeons
from classes.interfaces import Interface, MapInter, MainMenu, InventoryInter, Settings, ConsoleGui
from scripts.Console import *

polygon = generate_dungeons()

tick = 0
draw_grid = False
cur_inter = None

game_manager = GameManager((display_width, display_height),
                           polygon, curr_room)
heretic = Heretic(100, 100, 75, 100, 100, random.choice(directions), game_manager)

player_manager = PlayerManager(heretic)

console = Console(game_manager, player_manager)

Map = MapInter(polygon, game_manager)
Inventory = InventoryInter(heretic, game_manager)
Menu = MainMenu(game_manager)

print(*[''.join([str(i).rjust(3) for i in list(range(1 + dung_length * i,
                                                     dung_length * (i + 1) + 1))]) for i in range(dung_width)],
      sep='\n')

wipe = pygame.USEREVENT + 1
show_paths = pygame.USEREVENT + 2
pygame.time.set_timer(wipe, 10)
pygame.time.set_timer(show_paths, 150)
clock = pygame.time.Clock()
logging.info('The game cycle has begun')

while game_cycle:
    cur_room = game_manager.dungeon[game_manager.curr_room]
    for event in pygame.event.get():
        if event.type == wipe:
            cur_room.clear()
            # print(heretic.collised_walls, heretic.speed_directions)
        elif event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == show_paths:
            cur_room.make_paths(heretic)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                if isinstance(cur_inter, MapInter):
                    cur_inter = None
                else:
                    cur_inter = Map

            elif event.key == pygame.K_i:
                if isinstance(cur_inter, InventoryInter):
                    cur_inter = None
                    Inventory.close()
                    print(heretic.inventory)
                else:
                    cur_inter = Inventory
                    Inventory.open()

            elif event.key == pygame.K_e:
                if isinstance(heretic.weapon, Melee):
                    cur_room.decors.extend(heretic.hit(cur_room.entities_list,
                            cur_room.containers))
                elif isinstance(heretic.weapon, LongRange):
                    proj = heretic.shoot()
                    if proj is not None:
                        cur_room.projectiles.append(proj)

            elif event.key == pygame.K_g:
                draw_grid = ~draw_grid

            elif event.key == pygame.K_ESCAPE:
                game_manager.state = 'main_menu'

            elif event.key == pygame.K_SLASH:
                ConsoleGui(console)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if isinstance(cur_inter, InventoryInter):
                cur_inter.process(event.button, pygame.mouse.get_pos())
            if event.button == 1:
                if game_manager.state == 'main_menu':
                    Menu.process(pygame.mouse.get_pos())

    if game_manager.state == 'main_menu':
        Menu.draw_object(game_manager.display)

    elif game_manager.state == 'settings':
        print('set')

    elif game_manager.state == 'main_game':
        cur_room.draw_object(game_manager.display, tick, draw_grid)
        heretic.draw_object(game_manager.display)

        game_manager.display.blit(text_font.render(f'{game_manager.curr_room}', True, WHITE), (25, 25))
        game_manager.display.blit(text_font.render(f'{heretic.money}', True, '#f8b800'), (25, 55))
        if isinstance(cur_inter, Interface):
            cur_inter.draw_object(game_manager.display)

        elif not game_manager.is_paused:
            heretic.move()
            heretic.update(tick, cur_room.is_safe)
            cur_room.life(tick)
            cur_room.physics(heretic)

    pygame.display.update()

    clock.tick(60)
    tick += 1
    cur_room.visited = True
