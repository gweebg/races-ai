import os
import sys
import threading

import pygame

from src.app.button import Button
from src.mapper.simulator import Simulator

BG_COLOR = '#DCDDD8'  # c8d8e3


class Game:

    def __init__(self, maps_path: str):
        # Let's, firstly, setup our pygame configuration!
        pygame.init()
        pygame.display.set_caption("Vector Race Minecraft Edition")

        self.width, self.height = 350, 425
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)

        # Every map found on the map folder, and which map is currently selected.
        self.map_path = maps_path
        self.maps = self.get_maps(maps_path)
        self.map_index = 0

        # Every algorithm implemented, and which algorithm is currently selected.
        self.algorithms = ["Greedy", "BFS", "DFS", "A*"]
        self.algorithm_index = 0

        # Possible car numbers, and how many cars are selected.
        self.cars = [1, 2, 3, 4]
        self.car_index = 0
        self.car_colors = [
            (255, 0, 0, 100),
            (0, 0, 255, 100),
            (245, 66, 236, 100),
            (255, 255, 255, 150)
        ]

        # Represents the state of the application, if it's running the simulation or not.
        self.simulating = False

    @staticmethod
    def get_maps(maps_path: str) -> list[str]:

        # Checking whether the path exists or not.
        if not os.path.exists(maps_path):
            print("An error occurred while reading maps from folder.")
            SystemExit(0)

        return [file[:-4].replace('_', ' ').title() for file in os.listdir(maps_path) if file.startswith('map')]

    def add_text(self, text: str, pos: tuple, color: str = '#545454'):

        text_surf = self.font.render(text, True, color)

        text_rect = text_surf.get_rect()
        text_rect.center = pos

        self.screen.blit(text_surf, text_rect)

        return text_rect.centerx, text_rect.width

    def next_selection(self, where_list: str, where_index: str):

        list_selection: list = getattr(self, where_list)
        index: int = getattr(self, where_index)

        if index == len(list_selection) - 1:
            setattr(self, where_index, 0)
        else:
            setattr(self, where_index, index + 1)

    def prev_selection(self, where_list: str, where_index: str):

        list_selection: list = getattr(self, where_list)
        index: int = getattr(self, where_index)

        if index == 0:
            setattr(self, where_index, len(list_selection) - 1)
        else:
            setattr(self, where_index, index - 1)

    def start_handle(self):

        self.simulating = True

    def compute_resolution(self, threading_event: threading.Event, output: list):

        map_path = self.map_path + self.maps[self.map_index].lower().replace(" ", "_") + ".txt"

        algorithm = self.algorithms[self.algorithm_index]
        cars = self.cars[self.car_index]

        print("COMPUTING!")

        paths, tile_map = Simulator(map_path, algorithm, cars).get_resources()

        print("DONE!")

        output.append(paths)
        output.append(tile_map)

        threading_event.set()

    def run(self):

        # Buttons for the map selection!
        prev_map = Button('<', 40, 40, 6, self.screen, self.font)
        prev_map.set_handle(self.prev_selection, 'maps', 'map_index')

        next_map = Button('>', 40, 40, 6, self.screen, self.font)
        next_map.set_handle(self.next_selection, 'maps', 'map_index')

        # Buttons for the number of cars selection!
        prev_car = Button('<', 40, 40, 6, self.screen, self.font)
        prev_car.set_handle(self.prev_selection, 'cars', 'car_index')

        next_car = Button('>', 40, 40, 6, self.screen, self.font)
        next_car.set_handle(self.next_selection, 'cars', 'car_index')

        # Buttons for the algorithm selection!
        prev_alg = Button('<', 40, 40, 6, self.screen, self.font)
        prev_alg.set_handle(self.prev_selection, 'algorithms', 'algorithm_index')

        next_alg = Button('>', 40, 40, 6, self.screen, self.font)
        next_alg.set_handle(self.next_selection, 'algorithms', 'algorithm_index')

        # Start app button!
        start = Button('Start Game!', 200, 40, 6, self.screen, self.font)
        start.set_position((self.width / 2 - 100, 320))
        start.set_handle(self.start_handle)

        # Application Logo!

        title_font_name = "../docs/assets/HarlowSolidPlain.otf"
        title_font = pygame.font.Font(title_font_name, 50)

        # Credits!

        credit_font = pygame.font.Font(None, 20)
        credit_font_smaller = pygame.font.Font(None, 15)

        running = False
        processing = False

        while True:

            # Handling events!
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    # Events only for the simulation part.
                    if self.simulating and running:

                        if event.key == pygame.K_q:
                            self.screen = pygame.display.set_mode((self.width, self.height))
                            self.simulating = False

                            start.enable()
                            running = False

                        if event.key == pygame.K_r:
                            self.screen.blit(tile_map.map_surface, (0, 0))
                            path_counter = 0

                        if event.key == pygame.K_RIGHT:

                            for i in range(len(paths)):
                                path = paths[i]

                                if path_counter + 1 <= len(path[0]):

                                    pygame.draw.circle(self.screen,
                                                       self.car_colors[i],
                                                       (path[0][path_counter][0] * 64 - 32,
                                                        path[0][path_counter][1] * 64 - 32),
                                                       5)

                                    if path_counter > 0:
                                        prev_x, prev_y = path[0][path_counter - 1]
                                        curr_x, curr_y = path[0][path_counter]

                                        pygame.draw.line(self.screen,
                                                         self.car_colors[i],
                                                         (prev_x * 64 - 32, prev_y * 64 - 32),
                                                         (curr_x * 64 - 32, curr_y * 64 - 32),
                                                         3)

                            path_counter += 1

            # Main Menu Display, if the simulation is not running!
            if not running:

                self.screen.fill(BG_COLOR)

                # Drawing the title text!
                text_surf = title_font.render("Vector Race", True, '#475F77')

                text_rect = text_surf.get_rect()
                text_rect.center = (self.width / 2, 50)

                self.screen.blit(text_surf, text_rect)

                # Drawing the map selection prompt.
                m_x, m_width = self.add_text(
                    self.maps[self.map_index],
                    (self.width / 2, self.height / 2 - 120 + 20 + 15)
                )

                prev_map.set_position((m_x - m_width / 2 - 40 - 10, self.height / 2 - 120 + 20))
                next_map.set_position((m_x + m_width / 2 + 10, self.height / 2 - 120 + 20))

                prev_map.draw()
                next_map.draw()

                # Drawing the cars selection prompt.
                c_x, c_width = self.add_text(
                    str(self.cars[self.car_index]),
                    (self.width / 2, self.height / 2 + 20 + 15)
                )

                prev_car.set_position((c_x - c_width / 2 - 40 - 10, self.height / 2 + 20))
                next_car.set_position((c_x + c_width / 2 + 10, self.height / 2 + 20))

                prev_car.draw()
                next_car.draw()

                # Drawing the selection of algorithms.

                a_x, a_width = self.add_text(
                    self.algorithms[self.algorithm_index],
                    (self.width / 2, self.height / 2 + - 60 + 20 + 15)
                )

                prev_alg.set_position((a_x - a_width / 2 - 40 - 10, self.height / 2 - 60 + 20))
                next_alg.set_position((a_x + a_width / 2 + 10, self.height / 2 - 60 + 20))

                prev_alg.draw()
                next_alg.draw()

                # if self.car_index > 0 and self.algorithms[self.algorithm_index] == "DFS":
                #     start.disable()
                # else:
                #     start.enable()

                # Drawing the credits!
                text_surf = credit_font.render("Developed by:", True, '#545454')

                text_rect = text_surf.get_rect()
                text_rect.center = (self.width / 2, 390)

                self.screen.blit(text_surf, text_rect)

                text_surf = credit_font_smaller.render(
                    "Carlos Machado, Guilherme Sampaio, Tiago Oliveira",
                    True,
                    '#545454'
                )

                text_rect = text_surf.get_rect()
                text_rect.center = (self.width / 2, 405)

                self.screen.blit(text_surf, text_rect)

                text_surf = credit_font_smaller.render("Group 18", True, '#545454')

                text_rect = text_surf.get_rect()
                text_rect.center = (self.width / 2, 415)

                self.screen.blit(text_surf, text_rect)

                # Drawing start button!
                start.draw()

            # If the start button is clicked, then we set the state to simulating,
            # and compute de result for the selected items. We also set the running state to True.

            if self.simulating:

                if not running:

                    if not processing:

                        results = []
                        finish_event = threading.Event()

                        thread = threading.Thread(target=self.compute_resolution, args=(finish_event, results))
                        thread.start()

                        path_counter = 0

                        running = True
                        processing = True

                else:
                    if finish_event.is_set():
                        processing = False

                        paths, tile_map = results[0], results[1]
                        self.screen = pygame.display.set_mode((tile_map.map_w, tile_map.map_h))
                        self.screen.blit(tile_map.map_surface, (0, 0))

                        finish_event.clear()

            # Refreshing the screen (60 fps).
            pygame.display.update()
            self.clock.tick(60)
