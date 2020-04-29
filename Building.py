from Section import Section


def fetch_point_info(point, nodes_info):
    for item in nodes_info:
        if item[0].id == point.id:
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
    pass


def get_slope():
    pass


def calc_distance(point1, point2):
    '''return distance'''


def create_section_from_info(info):
    section = Section(info[0], get_end_point(), info[2], get_slope(), info[4], get_right_desc(info[0]), get_left_desc(info[0]),\
                      0, 0)
    return section


def diff(section1, section2):
    return (section1.ground_type != section2.ground_type) or (section1.is_steps != section2.is_steps)


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
        next_sec = create_section_from_info(fetch_point_info(point))
        if diff(sec, next_sec):
            sections.append(next_sec)
        sec = next_sec

    start_sec = sections[0]
    for section in sections[1:]:
        end_sec = section
        start_sec.end_point = end_sec.start_point
        start_sec.length = calc_distance(start_sec.start_point, start_sec.end_point)
        start_sec = end_sec
        
    return sections


def create_description(points_list) -> str:
    result = ""
    section_list = split_to_sections(points_list)
    result += section_list[0].get_section_description(None)
    for section_index in range(1, len(section_list) - 1):
        result += section_list[section_index].get_section_description(section_list[section_index - 1])
    return result
