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
    print(url)
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
    url = "http://api.openstreetmap.org/api/0.6/map?bbox=%s,%s,%s,%s" % (min(lon1,lon2), min(lat1,lat2), max(lon1,lon2),max(lat1, lat2))
    print(url)
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

def point_node_distance(point1,node1):
    p_lat = point1.lat
    p_lon = point1.lon
    n_lat = float(node1.get("lat"))
    n_lon = float(node1.get("lon"))
    return math.sqrt( (p_lat-n_lat)**2 + (p_lon-n_lon)**2)

def get_closest_node(point1):
    nodes = get_interesting_points(point1.lat,point1.lon,5);
    if not nodes:
        return -1
    max = 1000 # impossible distance between coordinates as max
    max_node = 0
    dist = 0
    for node in nodes:
        dist = point_node_distance(point1,node)
        if (dist < max):
            max = dist
            max_node = node
    return max_node


#points = Section.Point.create_points_list([[32.113254, 34.802280,7404723491]])
#print(get_closest_node(points[0]))
# print(get_interesting_points(32.112123, 34.803953,20))