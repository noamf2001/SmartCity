from ExampleInput import main_gate_to_stairs, with_turn, with_incline
from Section import Section
from OSMParser import create_nodes_info
from Section import Point
from TwoPoints import get_points_between_two_points

PATH = "map.osm"


def fetch_point_info(point, nodes_info):
    for item in nodes_info:
        if item["start_point"].id == point.id:
            return item


def get_right_desc(point):
    '''
    fetch other points from OSM to describe right side
    :return:
    '''
    pass


def get_left_desc(point):
    '''
    fetch other points from OSM to describe left side
    :return:
    '''
    pass


def get_end_point():
    return Point(0, 0, 0)


def get_slope():
    return 0


def create_section_from_info(info):
    section = Section(Point(0, 0, 0), Point(0, 0, 0), False, 0)
    if (info):
        section = Section(info["start_point"], get_end_point(), info["is_steps"], 0, info["ground_type"])
    return section


def diff(section1, section2):
    return (section1.ground_type != section2.ground_type) or (section1.is_steps != section2.is_steps)


def allNodes(points_list):
    allPoints = []
    l = len(points_list)
    for i in range(0, l - 1):
        allPoints.extend(get_points_between_two_points(points_list[i], points_list[i + 1]))
        print(len(allPoints))
        del allPoints[-1]

    return allPoints


def split_to_sections(points_list, nodes_info) -> list:
    """

    :param points_list: list of points of type Point (from Section)

    :return list of sections, such that each geographical parameter is valid to all of it
    """
    sections = []

    start = points_list[0]
    info = fetch_point_info(start, nodes_info)
    sec = create_section_from_info(info)
    sections.append(sec)

    for point in points_list[1:]:
        next_sec = create_section_from_info(fetch_point_info(point, nodes_info))
        if diff(sec, next_sec):
            sections.append(next_sec)
        sec = next_sec

    start_sec = sections[0]
    for section in sections[1:]:
        end_sec = section
        start_sec.end_point = end_sec.start_point
        start_sec.length = Point.calc_distance(start_sec.start_point, start_sec.end_point)
        start_sec = end_sec

    return sections


def create_description(points_list) -> str:
    """
    :param points_list: [[lat,lon,id] for every turn]
    :return: the text
    """
    result = ""
    points_list = Point.create_points_list(points_list)
    nodes_info = create_nodes_info(PATH)
    section_list = split_to_sections(allNodes(points_list), nodes_info)
    result += section_list[0].get_section_description(None)
    for section_index in range(1, len(section_list)):
        result += section_list[section_index].get_section_description(section_list[section_index - 1])

    return result


print(create_description(main_gate_to_stairs))
