from classes.surrounding import *
from scripts.algorithms_of_generation import generate_dungeons

heretic = Heretic(100, 100, 75, 100, 78, random.choice(directions), [])

polygon = generate_dungeons()
print(*[''.join([str(i).rjust(3) for i in list(range(1 + dung_length * i, dung_length * (i + 1) + 1))]) for i in
        range(dung_width)], sep='\n')

sp_ev = pygame.USEREVENT + 1
show_speed = pygame.time.set_timer(sp_ev, 60)
clock = pygame.time.Clock()

while game_cycle:
    for event in pygame.event.get():
        if event.type == sp_ev:
            print(c_a_s.curr_room)
        if event.type == pygame.QUIT:
            pygame.quit()

    polygon[c_a_s.curr_room].draw_object(display)
    heretic.draw_object(display)

    pygame.draw.rect(display, '#FF0000', left_border)
    pygame.draw.rect(display, '#FF0000', right_border)
    pygame.draw.rect(display, '#FF0000', upper_border)
    pygame.draw.rect(display, '#FF0000', lower_border)
    pygame.display.update()

    heretic.move()
    polygon[c_a_s.curr_room].life()
    polygon[c_a_s.curr_room].physics(heretic)

    clock.tick(60)
