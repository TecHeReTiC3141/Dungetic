import pygame

pygame.init()
dung_length, dung_width = map(int, input('Введите длину и ширину подземелья: ').split())
curr_room = random.randint(1, dung_width * dung_length)

display_width, display_height = (1440, 800)
clock = pygame.time.Clock()
directions = 'left right up down'.split()
opposites = ['right', 'left', 'dowm', 'up']

tick = 0

BLACK = '#000000'
WHITE = '#FFFFFF'
RED = '#FF0000'
GREEN = '#00FF00'
BLUE = '#0000FF'

# images and surfaces
map_image = pygame.image.load('./images/old_map2.jpg').convert_alpha()
cursor_for_battle = pygame.image.load('./images/sword.png')
cursor_for_battle = pygame.transform.scale(cursor_for_battle,
                                           (cursor_for_battle.get_width() // 5, cursor_for_battle.get_height() // 5))
map_image = pygame.transform.scale(map_image, (
    int(map_image.get_width() / 1.5), int(map_image.get_height() * 0.6))).convert_alpha()

stone_floor = pygame.transform.scale(pygame.image.load('./images/stone_floor.jpg'), (display_width, display_height))
heretic_images = {i: pygame.image.load(f'../images/heretic_sprite_{i}.png') for i in directions}
bloor = pygame.Surface((display_width, display_height))
bloor.set_alpha(15)
current_interface = None

# fonts
text_font = pygame.font.Font(None, 40)
active_font = pygame.font.Font(None, 50)
inventory_font = pygame.font.SysFont('Cambria', 75)
