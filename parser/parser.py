# class MapObjectType(Enum):
#     WALL = 0
#     START = 1
#     FINAL = 2
#     PATH = 3
#
#     @classmethod
#     def match(cls, char) -> 'MapObjectType':
#
#         if char == 'X':
#             return MapObjectType.WALL
#
#         if char == '-':
#             return MapObjectType.PATH
#
#         if char == 'P':
#             return MapObjectType.START
#
#         if char == 'F':
#             return MapObjectType.FINAL

# class MapObject:
#
#     def __init__(self, coord_x: int, coord_y: int, obj_type: MapObjectType):
#         self.x = coord_x
#         self.y = coord_y
#         self.type = obj_type
#
#     def __eq__(self, other: 'MapObject'):
#
#         if self.x == other.x and self.y == other.y and self.type == other.type:
#             return True
#
#         return False
#
#     def __repr__(self):
#         return f"{self.type.name}.{self.x}.{self.y}"


def parse_map(path_to_map: str):

    result_map = {}

    with open(path_to_map, "r") as map_file:
        lines = map_file.readlines()

    current_line = 0
    current_char = 0

    for line in lines:
        line = line.replace('\n', '').replace(' ', '')

        for char in line:
            result_map[(current_char, current_line)] = char
            current_char += 1

        current_line += 1

    return result_map


# def main():
#     result_map = parse_map('/home/guilherme/Documents/repos/races-ai/docs/map_a.txt')
#     print(result_map)
#
#
# if __name__ == "__main__":
#     SystemExit(main())
