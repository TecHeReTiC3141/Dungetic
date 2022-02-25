from classes.Heretic import *

heretic = Heretic(100, 100, 75, 100, 78, random.choice(directions), [])

direction = 'left right up down'.split()

clock = pygame.time.Clock()

while game_cycle:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    display.fill((218, 150, 61))
    heretic.draw_object(display)
    heretic.move()
    pygame.display.update()
    clock.tick(60)
