from Parser import split_to_sections


def create_description(points_list) -> str:
    result = ""
    section_list = split_to_sections(points_list)
    result += section_list[0].get_section_description(None)
    for section_index in range(1,len(section_list) - 1):
        result += section_list[section_index].get_section_description(section_list[section_index - 1])
    return result
