from typing import List
from building import Point


class Section:
    def __init__(self, start_point: Point, end_point: Point):
        pass

    def get_section_description(self) -> str:
        pass

    @staticmethod
    def get_sections_transition_description(from_section, to_section) -> str:
        pass


def get_objects_around_line(start_point: Point, end_point: Point):
    pass


def split_line_points(start_point: Point, end_point: Point) -> List[Section]:
    """

    :param start_point:
    :param end_point:

    :return list of sections, so that every section is one kind of description
    """
    pass


def build_line_description(start_point: Point, end_point: Point) -> str:
    result = ""
    section_list = split_line_points(start_point, end_point)
    for section_index in range(len(section_list) - 1):
        result += section_list[section_index].get_section_description()
        result += Section.get_sections_transition_description(section_list[section_index],
                                                              section_list[section_index + 1])
    result += section_list[len(section_list) - 1].get_section_description()
    return result
