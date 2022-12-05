import os

import pygame

from rich.console import Console
from rich.prompt import Prompt, IntPrompt

from mapper.tiles import TileMap
from parser.parser import parse_map
from path_gen.path_gen import generate_player_graph, CircuitNode, Car

# Console pretty printer. #

console = Console()

# Important constants. #

maps = './docs/maps'
# available_algorithms = ["DFS", "BFS", "A*", "Greedy"]
available_algorithms = ["DFS"]


# Returns a list containing every map file in the provided path.
def get_maps(maps_path: str) -> list[str]:
    if not os.path.exists(maps_path):
        console.print("[red]Invalid map folder path![/]", style="bold")

    return [file for file in os.listdir(maps_path) if file.startswith('map')]


# Greets the user and asks him to choose the map to simulate on.
def main_menu() -> tuple[TileMap, str]:
    console.print("[bold]\nWelcome to Vector Race Minecraft Map Simulator or [cyan]VRMMP[/] for short![/]")
    console.print("[bold]Choose a [red]map[/] from the ones listed bellow![/]")

    map_list = get_maps(maps)
    for i, map_name in enumerate(map_list):
        console.print(f"  [bold cyan]{i}.[/] {map_name}")

    chosen_map = IntPrompt.ask("[bold]I want map [red]number[/][/]", choices=[str(num) for num in range(len(map_list))])

    return TileMap(maps + f"/{map_list[chosen_map]}", None), f"{maps}/{map_list[chosen_map]}"


# Ask the user which algorithm he wants to use.
def prompt_algorithm() -> str:
    console.print("\n[bold]Which [cyan]algorithm[/] do you want to use ?[/]")

    for i, algo in enumerate(available_algorithms):
        console.print(f"  [bold cyan]{i}.[/] {algo}")

    algorithm = Prompt.ask("[bold]I choose[/]", choices=[str(num) for num in range(len(available_algorithms))])
    return available_algorithms[int(algorithm)]


def prompt_simulate() -> int:
    console.print("\n[bold]Please [red]choose[/] what to do![/]")

    console.print("  [bold cyan]0.[/] Run graphic interface.")
    console.print("  [bold cyan]1.[/] Print found path.")
    console.print("  [bold cyan]2.[/] Print generated graph.")
    console.print("  [bold cyan]3.[/] Exit.")

    option = IntPrompt.ask("What's it gonna be", choices=[str(num) for num in range(4)])
    return option


def run_graphical(my_map: TileMap, path: list[tuple[int,int]]):
    # Setting game variables. #

    pygame.init()

    DISPLAY_W, DISPLAY_H = my_map.map_w, my_map.map_h

    canvas = pygame.Surface((DISPLAY_W, DISPLAY_H), pygame.SRCALPHA)
    window = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))

    clock = pygame.time.Clock()

    # Starting game loop. #

    # path = [(9, 2), (8, 3), (7, 3), (6, 4), (6, 5), (6, 6), (7, 7), (8, 8), (9, 9), (9, 10)]
    path_counter = 0
    path_length = len(path)

    canvas.fill((0, 180, 240))  # Painting the canvas just in case.
    my_map.draw_map(canvas)  # Drawing our tile map.

    running = True
    while running:

        clock.tick(60)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if path_counter + 1 <= path_length:

                        pygame.draw.circle(canvas,
                                           (245, 66, 236, 100),
                                           (path[path_counter][0] * 64 - 32, path[path_counter][1] * 64 - 32),
                                           5)

                        if path_counter > 0:
                            prev_x, prev_y = path[path_counter - 1]
                            curr_x, curr_y = path[path_counter]

                            pygame.draw.line(canvas,
                                             (245, 66, 236, 100),
                                             (prev_x * 64 - 32, prev_y * 64 - 32),
                                             (curr_x * 64 - 32, curr_y * 64 - 32),
                                             3)

                        path_counter += 1

                if event.key == pygame.K_r:
                    canvas.fill((0, 180, 240))
                    my_map.draw_map(canvas)
                    path_counter = 0

        window.blit(canvas, (0, 0))
        pygame.display.update()

def path_coordinates(path):
    coord_list = []

    for i in range(1, len(path)):
        node1 = path[i-1]
        node2 = path[i]
        nx = node1.car.pos_x
        ny = node1.car.pos_y
        endx = node2.car.pos_x
        endy = node2.car.pos_y
        xdir = max(-1, min(node2.car.pos_x - node1.car.pos_x, 1))
        ydir = max(-1, min(node2.car.pos_y - node1.car.pos_y, 1))

        coord_list.append((nx + 1, ny + 1))
        while nx != endx or ny != endy:
            if nx != endx:
                nx += xdir
            if ny != endy:
                ny += ydir

            coord_list.append((nx + 1, ny + 1))

    return coord_list

# Run the simulation.
def main():
    my_map, map_path = main_menu()  # Load the Map via console prompt.
    algorithm: str = prompt_algorithm()  # Get which algorithm to use on the path.

    circuit, start_pos, finish_pos_list = parse_map(map_path)
    graph = generate_player_graph(circuit, start_pos[0], start_pos[1])

    st = CircuitNode(Car(pos_x=start_pos[0], pos_y=start_pos[1]), circuit[start_pos[1]][start_pos[0]])
    f_pos = finish_pos_list[2]
    end = CircuitNode(Car(pos_x=f_pos[0], pos_y=f_pos[1]), circuit[f_pos[1]][f_pos[0]])

    if algorithm == 'DFS':
        path, cost = graph.dfs(st, end)

    path = path_coordinates(path)

    console.print("[bold green]\nFinished setting up the simulation![/]")
    running = True


    while running:
        next_action = prompt_simulate()

        if next_action == 0:
            run_graphical(my_map, path)
            running = False

        if next_action == 1:
            console.print("Found this path:")
            console.print(path)
            console.print(f"[bold]With the [green]cost[/] of: [yellow]{cost}[/][/]")

        if next_action == 2:
            console.print("[bold red]Not yet implemented.[/]")

        if next_action == 3:
            running = False


if __name__ == "__main__":
    SystemExit(main())
