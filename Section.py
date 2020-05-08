import numpy as np
import math

# radius of the Earth
R = 6373.0


class Point:
    def __init__(self, id, lat, lon):
        self.id = id
        self.lat = lat
        self.lon = lon

    def get_angle(self, other_point):
        dlon = self.lon - other_point.lon
        y = math.sin(dlon) * math.cos(other_point.lat)
        x = math.cos(self.lat) * math.sin(other_point.lat2) - math.sin(self.lat) * math.cos(other_point.lat) * math.cos(
            dlon)
        brng = math.atan2(y, x)
        brng = math.degrees(brng)
        brng = (brng + 360) % 360
        brng = 360 - brng  # count degrees counter - clockwise - remove to make clockwise
        return brng

    @staticmethod
    def sub_points(point1, point2):
        return Point(0, point2.lat - point1.lat, point2.lon - point1.lon)

    @staticmethod
    def calc_distance(point1, point2):
        lat1 = math.radians(point1.lat)
        lon1 = math.radians(point1.lon)
        lat2 = math.radians(point2.lat)
        lon2 = math.radians(point2.lon)

        dlon = lon2 - lon1

        dlat = lat2 - lat1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance

    @staticmethod
    def create_points_list(points_list):
        new_points_list = []
        for point in points_list:
            new_points_list.append(Point(point[2], point[0], point[1]))
        return new_points_list


class Section:
    def __init__(self, start_point: Point, end_point: Point, ground_type: str, slope: int, is_steps: bool,
                 r_side_description: str, l_side_description: str, length: int,
                 steps_num: int = 0, rail: str = "N", stairs_slope: str = "N", block: str = "", comments: str = ""):
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
        self.steps_num = steps_num  # 8
        self.rail = rail  # 9
        self.stairs_slope = stairs_slope  # 10
        self.block = block  # 11
        self.comments = comments  # 12

        self.angle = Point.sub_points(end_point, start_point).get_angle()

    def create_turn_description(self, prev_angle) -> str:

        turn_angle = self.angle - prev_angle
        if turn_angle > 180:
            turn_angle = 360 - turn_angle
            direction = "left"
        elif 0 < turn_angle <= 180:
            direction = "right"
        elif -180 < turn_angle < 0:
            turn_angle *= -1
            direction = "left"
        else:  # turn_angle < -180
            turn_angle += 360
            direction = "right"
        return "turn " + str(turn_angle) + " degrees " + direction

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

    def create_block_description(self) -> str:
        return "there is a blocking object ahead: " + self.block

    def create_comments_description(self) -> str:
        return "here is some information about your road" + self.comments

    def get_section_description(self, prev_section=None):
        result = ""
        if prev_section is not None and self.angle != prev_section.angle:
            result += self.create_turn_description(prev_section.current_incline) + "\n"

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
        if prev_section is not None and prev_section.block != self.block and self.block != "":
            result += self.create_length_description() + "\n"
        if self.comments != "" and prev_section is not None and prev_section.comments != self.comments:
            result += self.create_comments_description() + "\n"
        return result
