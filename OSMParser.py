from osmread import parse_file, Node, Way
from Section import Point


def osmToEntities(path: str):
    entities = []
    for entity in parse_file(path):
        if entity.tags:
            entities.append(entity)
    return entities


def createNodes(entities):
    nodes = []
    for entity in entities:
        if isinstance(entity, Node):
            # node = OSMNode(entity.id, entity.lon, entity.lat)
            nodes.append(entity)
    return nodes


def createWays(entities):
    ways = []
    for entity in entities:
        if isinstance(entity, Way):
            # way = OSMWay(entity.id, entity.nodes)
            ways.append(entity)
    return ways


def createOutputList(nodes, ways):
    output = []

    for i, item in enumerate(nodes):
        node_tags = [None] * 14
        start_point = Point(item.id, item.lon, item.lat)
        node_tags[0] = start_point

        if "highway" in item.tags:
            node_tags[9] = item.tags["highway"]

        if "amenity" in item.tags:
            node_tags[7] = item.tags["amenity"]

        for way in ways:
            if item.id in way.nodes:

                # write way highway-type
                if "highway" in way.tags:
                    node_tags[2] = way.tags["highway"]
                    if way.tags["highway"] == "steps":
                        node_tags[4] = "Yes"

                # write way handrail
                if "handrail" in way.tags:
                    node_tags[5] = way.tags["handrail"]

                # write way step-count
                if "step_count" in way.tags:
                    node_tags[10] = way.tags["step_count"]

                # write way barrier
                if "barrier" in way.tags:
                    node_tags[3] = way.tags["barrier"]

                # write way name
                if "name:en" in way.tags:
                    node_tags[5] = way.tags["name:en"]

        output.append(node_tags)
    return output


def writeNodesToFile(nodes, name, sheet, book):
    for i, node in enumerate(nodes):
        cell = "A" + str(i)
        print(str(node.id))
        print(sheet[cell])
        sheet[cell] = str(node.id)
    book.save(name)


def create_nodes_info(path:str):
    entities = osmToEntities(path)
    nodes = createNodes(entities)
    ways = createWays(entities)
    nodes_info = createOutputList(nodes, ways)
    return nodes_info
