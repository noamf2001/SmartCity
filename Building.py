def fetch_point_info(point, nodes_info):
    for item in nodes_info:
        if item[0].id == point.id:
            return item


def create_section_from_info(info):
    pass


def diff(section1, section2):
    pass


def split_to_sections(points_list, nodes_info) -> list:
    """

    :param start_point:
    :param end_point:

    :return list of sections, so that every section is one kind of description
    """
    sections = []

    start = points_list[0]
    info = fetch_point_info(start)
    sec = create_section_from_info(info)
    sections.append(sec)

    for point in points_list[1:]:
        next_sec = create_section_from_info(fetch_point_info(point))
        if diff(sec, next_sec):
            sections.append(next_sec)
        sec = next_sec

    return sections


def create_description(points_list) -> str:
    result = ""
    section_list = split_to_sections(points_list)
    result += section_list[0].get_section_description(None)
    for section_index in range(1, len(section_list) - 1):
        result += section_list[section_index].get_section_description(section_list[section_index - 1])
    return result
