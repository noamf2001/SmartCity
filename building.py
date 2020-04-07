class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y



def create_description(points_list) -> str:
    result = ""
    for current_point_index in range(len(points_list) - 1):
        result += build_turn_description(points_list[current_point_index], points_list[current_point_index + 1])
        result += build_straight_line_description(points_list[current_point_index],
                                                  points_list[current_point_index + 1])
    return result
