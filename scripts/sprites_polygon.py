from classes.Heretic import *
from classes.surrounding import *

heretic = Heretic(100, 100, 75, 100, 78, random.choice(directions), [])
vase = Vase(random.randint(100, display_width), random.randint(100, display_height), 50, 50)
pygame.image.save(vase.draw_object(display), '../images/vase_sprite.png')
direction = 'left right up down'.split()

clock = pygame.time.Clock()

while game_cycle:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    display.fill((218, 150, 61))
    vase.draw_object(display)
    heretic.draw_object(display)
    heretic.move()
    pygame.display.update()
    clock.tick(60)
