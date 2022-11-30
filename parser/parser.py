from enum import Enum


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

class MapPiece(Enum):
    TRACK = 0
    OUTSIDE_TRACK = 1
    START = 2
    FINISH = 3

    def is_inside_track(self):
        match self:
            case MapPiece.TRACK | MapPiece.FINISH | MapPiece.START:
                return True
            case _:
                return False

    def travel_cost(self, other):
        if other.is_inside_track():
            return 1
        else:
            return 25

    @classmethod
    def match_char(cls, char) -> 'MapPiece':
        if char == 'X':
            return MapPiece.OUTSIDE_TRACK

        if char == '-':
            return MapPiece.TRACK

        if char == 'P':
            return MapPiece.START

        if char == 'F':
            return MapPiece.FINISH


def parse_map(path_to_map: str):
    result_list = []
    start_pos = None
    finish_pos_list = []

    with open(path_to_map, "r") as map_file:
        lines = map_file.readlines()

    current_line = 0
    for line in lines:
        line = line.replace('\n', '').replace(' ', '')
        current_char = 0
        result_list.append([])
        for char in line:
            piece = MapPiece.match_char(char)
            if piece is MapPiece.START:
                start_pos = (current_char, current_line)
            if piece is MapPiece.FINISH:
                finish_pos_list.append((current_char, current_line))

            result_list[current_line].append(piece)
            current_char += 1

        current_line += 1

    return result_list, start_pos, finish_pos_list

# def main():
#     result_map = parse_map('/home/guilherme/Documents/repos/races-ai/docs/map_a.txt')
#     print(result_map)
#
#
# if __name__ == "__main__":
#     SystemExit(main())
