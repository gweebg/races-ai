from tiles import *

# Load map.

my_map = TileMap('/home/guilherme/Documents/repos/races-ai/docs/map_a.txt', None)

# Load up a basic window and clock.

pygame.init()
DISPLAY_W, DISPLAY_H = my_map.map_w, my_map.map_h
canvas = pygame.Surface((DISPLAY_W, DISPLAY_H))
window = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
running = True
clock = pygame.time.Clock()

# Game loop.

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            pass

    canvas.fill((0, 180, 240))
    my_map.draw_map(canvas)
    window.blit(canvas, (0, 0))
    pygame.display.update()

