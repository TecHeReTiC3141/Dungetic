from classes.surrounding import *
from scripts.algorithms_of_generation import generate_dungeons
from classes.interfaces import Interface, MapInter, MainMenu
from scripts.game_manager import GameManager

heretic = Heretic(100, 100, 75, 100, 78, random.choice(directions), [])
game_manager = GameManager()

polygon = generate_dungeons()

cur_inter = None
Map = MapInter(polygon)
Menu = MainMenu(game_manager)

print(*[''.join([str(i).rjust(3) for i in list(range(1 + dung_length * i,
                                                     dung_length * (i + 1) + 1))]) for i in range(dung_width)],
      sep='\n')

sp_ev = pygame.USEREVENT + 1
pygame.time.set_timer(sp_ev, 180)
clock = pygame.time.Clock()

while game_cycle:
    for event in pygame.event.get():
        if event.type == sp_ev:
            polygon[c_a_s.curr_room].clear()
            # print(heretic.collised_walls, heretic.speed_directions)
        elif event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                if isinstance(cur_inter, MapInter):
                    cur_inter = None
                else:
                    cur_inter = Map

            elif event.key == pygame.K_g:
                game_manager.state = 'main_game'

            elif event.key == pygame.K_e:
                heretic.hit(polygon[c_a_s.curr_room].entities_list,
                            polygon[c_a_s.curr_room].containers)

            elif event.key == pygame.K_ESCAPE:
                game_manager.state = 'main_menu'

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if game_manager.state == 'main_menu':
                    Menu.process(pygame.mouse.get_pos())

    if game_manager.state == 'main_menu':
        Menu.draw_object(display)

    elif game_manager.state == 'main_game':
        polygon[c_a_s.curr_room].draw_object(display)
        heretic.draw_object(display)

        pygame.draw.rect(display, '#FF0000', left_border)
        pygame.draw.rect(display, '#FF0000', right_border)
        pygame.draw.rect(display, '#FF0000', upper_border)
        pygame.draw.rect(display, '#FF0000', lower_border)
        display.blit(text_font.render(f'{c_a_s.curr_room}', True, WHITE), (25, 25))
        if isinstance(cur_inter, Interface):
            cur_inter.draw_object(display)
        heretic.move()
        heretic.update()
        polygon[c_a_s.curr_room].life()
        polygon[c_a_s.curr_room].physics(heretic)

    pygame.display.update()

    clock.tick(60)

    polygon[c_a_s.curr_room].visited = True
