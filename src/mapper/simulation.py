import sys

import pygame
import pickle

from src.mapper.tiles import TileMap


class Simulation:

    def __init__(self, my_map: TileMap, paths: list[list[tuple[int, int]]]):

        # PyGame Initialization #

        pygame.init()

        self.display_w, self.display_h = my_map.map_w, my_map.map_h

        self.canvas = pygame.Surface((self.display_w, self.display_h), pygame.SRCALPHA)
        self.window = pygame.display.set_mode((self.display_w, self.display_h), pygame.NOFRAME)

        self.clock = pygame.time.Clock()

        # Logic Initialization #

        self.path_counter = 0
        self.path_length = len(paths)

        self.my_map = my_map
        self.paths = paths

    def simulate(self):

        self.my_map.draw_map(self.canvas)

        running = True
        while running:

            self.clock.tick(60)
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if self.path_counter + 1 <= self.path_length:
                            for path in self.paths:
                                pygame.draw.circle(self.canvas,
                                                   (245, 66, 236, 100),
                                                   (path[self.path_counter][0] * 64 - 32,
                                                    path[self.path_counter][1] * 64 - 32),
                                                   5)

                                if self.path_counter > 0:
                                    prev_x, prev_y = path[self.path_counter - 1]
                                    curr_x, curr_y = path[self.path_counter]

                                    pygame.draw.line(self.canvas,
                                                     (245, 66, 236, 100),
                                                     (prev_x * 64 - 32, prev_y * 64 - 32),
                                                     (curr_x * 64 - 32, curr_y * 64 - 32),
                                                     3)

                                self.path_counter += 1

                    if event.key == pygame.K_r:
                        self.my_map.draw_map(self.canvas)
                        self.path_counter = 0

                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        pygame.quit()
                        return

            self.window.blit(self.canvas, (0, 0))
            pygame.display.update()


# def main():
#
#     tile_map_data = sys.argv[1]
#     path_data = sys.argv[2]
#
#     tile_map: TileMap = pickle.loads(tile_map_data)
#     path: list[tuple[int, int]] = pickle.loads(path_data)
#
#
# if __name__ == "__main__":
#     SystemExit(main())
