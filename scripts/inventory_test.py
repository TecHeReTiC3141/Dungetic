from scripts.algorithms_of_generation import *
from classes.interfaces import *

heretic = Heretic(100, 100, 100, 100, 100, 'left', [])

inventory = Inventory(heretic)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    inventory.draw_object(display)
    pygame.display.update()