import urllib.request
import bs4
import time


def get_boundaries_box(lat, lon, meters):
    latmeters = 10 ** 8 / 899.0
    lonmeters = 10 ** 8 / 1268.0
    min_x, min_y = (lat - meters / latmeters, lon - meters / lonmeters)
    max_x, max_y = (lat + meters / latmeters, lon + meters / lonmeters)
    return (min_x, min_y), (max_x, max_y)


def get_interesting_points(lat, lon, meters):
    l = []
    (lat1, lon1), (lat2, lon2) = get_boundaries_box(lat, lon, meters)
    url = "http://api.openstreetmap.org/api/0.6/map?bbox=%s,%s,%s,%s" % (lon1, lat1, lon2, lat2)
    osm_text = urllib.request.urlopen(url).read()
    soup = bs4.BeautifulSoup(osm_text)
    nodes = soup.findAll("node")
    points = []
    for node in nodes:
        name_tag = node.find("tag")  # attrs={'k': 'name'})
        if name_tag:
            lat = float(node.get("lat"))
            lon = float(node.get("lon"))
            name = name_tag.get("v")
            timestamp = int(time.time())
            points.append(node)
    return points


def get_points_between_two_points(point1, point2):
    (lat1, lon1), (lat2, lon2) = (point1.lat, point1.lon), (point2.lat, point2.lon)
    url = "http://api.openstreetmap.org/api/0.6/map?bbox=%s,%s,%s,%s" % (lon1, lat1, lon2, lat2)
    osm_text = urllib.request.urlopen(url).read()
    soup = bs4.BeautifulSoup(osm_text)
    nodes = soup.findAll("node")
    points = []
    for node in nodes:
        name_tag = node.find("tag")  # attrs={'k': 'name'})
        if name_tag:
            lat = float(node.get("lat"))
            lon = float(node.get("lon"))
            name = name_tag.get("v")
            timestamp = int(time.time())
            points.append(node)
    return points


# print(get_interesting_points(32.112123, 34.803953,20))