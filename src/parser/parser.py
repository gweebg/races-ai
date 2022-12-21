from enum import Enum


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


def parse_map(path_to_map: str) -> tuple[list[list[MapPiece]], list[tuple[int, int]], list[tuple[int, int]]]:
    result_list = []
    start_pos_list = []
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
                start_pos_list.append((current_char, current_line))
            if piece is MapPiece.FINISH:
                finish_pos_list.append((current_char, current_line))

            result_list[current_line].append(piece)
            current_char += 1

        current_line += 1

    return result_list, start_pos_list, finish_pos_list
