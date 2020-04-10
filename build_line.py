from typing import List
from building import Point


class Section:
    def __init__(self, start_point: Point, end_point: Point, is_steps=False):
        self.start_point = start_point
        self.end_point = end_point
        self.incline = 0
        self.width = 0
        self.length = 0
        self.is_steps = is_steps
        self.railing = False
        self.steps_num = 0
        self.calc_width()
        self.calc_length()
        self.calc_incline()
        if self.is_steps:
            self.count_steps()
            self.is_railing()

    def is_railing(self):
        pass

    def count_steps(self):
        pass

    def calc_length(self):
        pass

    def calc_width(self):
        pass

    def calc_incline(self):
        pass

    def describe_left_roadside(self) -> str:
        pass

    def describe_right_roadside(self) -> str:
        pass

    def get_section_description(self) -> str:
        pass

    @staticmethod
    def get_sections_transition_description(from_section, to_section) -> str:
        pass


def get_objects_around_line(start_point: Point, end_point: Point) -> List[Point]:
    pass

def filter_useful_objects(points_list):
    pass

def split_line_points(start_point: Point, end_point: Point) -> List[Section]:
    """

    :param start_point:
    :param end_point:

    :return list of sections, so that every section is one kind of description
    """
    points_list = get_objects_around_line(start_point,end_point)
    filter_useful_objects(points_list)
    

def build_line_description(start_point: Point, end_point: Point) -> str:
    result = ""
    section_list = split_line_points(start_point, end_point)
    for section_index in range(len(section_list) - 1):
        result += section_list[section_index].get_section_description()
        result += Section.get_sections_transition_description(section_list[section_index],
                                                              section_list[section_index + 1])
    result += section_list[len(section_list) - 1].get_section_description()
    return result
