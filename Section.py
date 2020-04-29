class Point:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def get_angle(self, prev_point, prev_prev_point):

        pass


class Section:
    def __init__(self, start_point: Point, end_point: Point, ground_type: str, slope: int, is_steps: bool,
                 r_side_description: str, l_side_description: str, length: int, width: int,
                 turn_angle: int = 0, steps_num: int = 0, rail: str = "N", stairs_slope: str = "N", comments: str = ""):
        """
        :param rail: out of (N - no rail, "left","right")
        :param stairs_slope: out of ("N" - no stairs,"up","down")
        :param comments: no stairs comments
        """
        self.start_point = start_point  # 0
        self.end_point = end_point  # 1
        self.ground_type = ground_type  # 2
        self.slope = slope  # 3
        self.is_steps = is_steps  # 4
        self.r_side_description = r_side_description  # 5
        self.l_side_description = l_side_description  # 6
        self.length = length  # 7
        self.width = width  # 8
        self.turn_angle = turn_angle  # 9
        self.steps_num = steps_num  # 10
        self.rail = rail  # 11
        self.stairs_slope = stairs_slope  # 12
        self.comments = comments  # 13

    def create_turn_description(self) -> str:
        if self.turn_angle > 0:
            direction = "right"
        else:
            direction = "left"
        return "turn " + str(self.turn_angle) + " degrees " + direction

    def create_ground_type_description(self) -> str:
        return "the ground type is " + str(self.ground_type)

    def create_slope_description(self) -> str:
        return "there is a slope, and the angle is" + str(self.slope)

    def create_steps_description(self) -> str:
        result = "go" + self.stairs_slope + " " + str(self.steps_num) + "stairs"
        if self.rail != "N":
            result += "use the rail on the " + self.rail
        return result

    def create_r_side_description(self) -> str:
        return "in your right side you can find" + self.r_side_description

    def create_l_side_description(self) -> str:
        return "in your left side you can find" + self.l_side_description

    def create_length_description(self) -> str:
        return "the length of the road is" + str(self.length)

    def create_width_description(self) -> str:
        return "the width of the road is" + str(self.width)

    def create_comments_description(self) -> str:
        return "here is some information about your road" + self.comments

    def create_description(self, prev_section=None):
        result = ""
        if self.turn_angle != 0:
            result += self.create_turn_description() + "\n"

        if prev_section is not None and prev_section.ground_type != self.ground_type:
            result += self.create_ground_type_description() + "\n"
        if self.slope != 0 and prev_section is not None and prev_section.slope != self.slope:
            result += self.create_slope_description() + "\n"
        if self.is_steps:
            result += self.create_steps_description() + "\n"
        if prev_section is not None and prev_section.r_side_description != self.r_side_description:
            result += self.create_r_side_description() + "\n"
        if prev_section is not None and prev_section.l_side_description != self.l_side_description:
            result += self.create_l_side_description() + "\n"
        if prev_section is not None and prev_section.length != self.length:
            result += self.create_length_description() + "\n"
        if prev_section is not None and prev_section.width != self.width:
            result += self.create_width_description() + "\n"
        if self.comments != "" and prev_section is not None and prev_section.comments != self.comments:
            result += self.create_comments_description() + "\n"
        return result
