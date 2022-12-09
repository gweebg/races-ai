import os
from typing import Callable, Optional

from rich.console import Console
from rich.progress import Progress
from rich.prompt import Prompt, IntPrompt

from src.graph.graph import Graph
from src.mapper.tiles import TileMap
from src.models.race_car import RaceCar, Coordinates
from src.parser.parser import parse_map
from src.mapper.path_gen import generate_paths_graph, CircuitNode

from src.mapper.simulation import Simulation


class Application:

    def __init__(self, map_folder_path: str) -> None:

        self.algorithm = None
        self.tile_map = None
        self.path = None
        self.cost = None

        self.maps_path = map_folder_path
        self.maps: list[str] = self.get_maps(map_folder_path)

        self.console = Console()

        self.graph: tuple[Graph, CircuitNode, list[CircuitNode]] = self.build_graph()

        self.algorithm_map: dict[str, Callable[[CircuitNode, list[CircuitNode]], Optional[tuple[list, int]]]] = {
            "DFS": self.graph[0].dfs_search,
            "BFS": self.graph[0].bfs_search,
            "Greedy": self.graph[0].greedy_search,
            "AStar": self.graph[0].a_star_search
        }

    def get_maps(self, maps_path: str) -> list[str]:
        if not os.path.exists(maps_path):
            self.console.print("[red]Invalid map folder path![/]", style="bold")

        return [file for file in os.listdir(maps_path) if file.startswith('map')]

    def prompt_map(self) -> tuple[TileMap, str]:

        self.console.print("[bold]\nWelcome to Vector Race Minecraft Map Simulator or [cyan]VRMMP[/] for short![/]")
        self.console.print("[bold]Choose a [red]map[/] from the ones listed bellow![/]")

        for i, map_name in enumerate(self.maps):
            self.console.print(f"  [bold cyan]{i}.[/] {map_name}")

        chosen_map = IntPrompt.ask("[bold]I want map [red]number[/][/]",
                                   choices=[str(num) for num in range(len(self.maps))])

        return TileMap(self.maps_path + f"/{self.maps[chosen_map]}"), f"{self.maps_path}/{self.maps[chosen_map]}"

    def prompt_graph(self, map_path: str) -> tuple[Graph, CircuitNode, list[CircuitNode]]:

        circuit, start_pos, finish_pos_list = parse_map(map_path)
        self.console.print("\n")

        with Progress(console=self.console) as progress:
            task = progress.add_task("[magenta bold]Generating Graph...", start=False, total=100)

            graph = generate_paths_graph(circuit, start_pos[0], start_pos[1], finish_pos_list)
            progress.update(task, advance=50)

            starting_node = CircuitNode(
                RaceCar(pos=Coordinates(x=start_pos[0], y=start_pos[1])),
                circuit[start_pos[1]][start_pos[0]]
            )
            progress.update(task, advance=20)

            finish_nodes: list[CircuitNode] = list(map(
                lambda pos:
                CircuitNode(RaceCar(pos=Coordinates(x=pos[0], y=pos[1])), circuit[pos[1]][pos[0]]),
                finish_pos_list
            ))

            progress.update(task, description="[blue]Done, Please Wait...", advance=30)
            progress.stop_task(task)

        return graph, starting_node, finish_nodes

    def build_graph(self) -> tuple[Graph, CircuitNode, list[CircuitNode]]:

        self.tile_map, map_path = self.prompt_map()
        return self.prompt_graph(map_path)

    def prompt_algorithm(self) -> str:
        self.console.print("\n[bold]Which [cyan]algorithm[/] do you want to use ?[/]")

        for i, algo in enumerate(self.algorithm_map.keys()):
            self.console.print(f"  [bold cyan]{i}.[/] {algo}")

        algorithm = Prompt.ask("[bold]I choose[/]", choices=[str(num) for num in range(len(self.algorithm_map))])

        return list(self.algorithm_map)[int(algorithm)]

    def prompt_action(self) -> int:

        self.console.print("\n[bold]Please [red]choose[/] what to do![/]")

        self.console.print("  [bold cyan]0.[/] Run graphic simulation!")
        self.console.print("  [bold cyan]1.[/] Check out the solution!")
        self.console.print("  [bold cyan]2.[/] Change the algorithm?")
        self.console.print("  [bold cyan]3.[/] Exit...")

        option = IntPrompt.ask("What's it gonna be", choices=[str(num) for num in range(4)])

        return option

    def print_path(self):
        self.console.print("Found this path:")
        strg = ""
        for i in range(0, len(self.path)):
            node = self.path[i]
            strg += f"Node {i}: pos: {node.car.pos}, acc: {node.car.acc}, vel: {node.car.vel}\n"
        self.console.print(strg)
        self.console.print(f"[bold]With the [green]cost[/] of: [yellow]{self.cost}[/][/]")

    @staticmethod
    def path_to_tuple(path: list[CircuitNode]) -> list[tuple[int, int]]:
        return [(node.car.pos.x + 1, node.car.pos.y + 1) for node in path]

    def run(self):

        self.console.print("\n", end='')

        self.path = None

        self.algorithm: str = self.prompt_algorithm()
        algorithm_func: Callable = self.algorithm_map.get(self.algorithm)

        self.path, self.cost = algorithm_func(self.graph[1], self.graph[2])

        tuple_path = self.path_to_tuple(self.path)

        reset, restart = False, False

        while True:

            if reset:
                self.algorithm: str = self.prompt_algorithm()
                algorithm_func: Callable = self.algorithm_map.get(self.algorithm)

                self.path, self.cost = algorithm_func(self.graph[1], self.graph[2])

                tuple_path = self.path_to_tuple(self.path)

            next_action: int = self.prompt_action()

            if next_action == 0:
                Simulation(self.tile_map, tuple_path).simulate()
                reset = False

            if next_action == 1:
                self.print_path()
                reset = False

            if next_action == 2:
                reset = True

            if next_action == 3:
                self.console.print("[bold yellow]Goodbye user :)")
                break


def main():

    app = Application('../../docs/maps')
    app.run()


if __name__ == '__main__':
    SystemExit(main())
