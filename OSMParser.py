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
        node_tags = {}
        start_point = Point(item.lat,item.lon,item.id)
        node_tags["start_point"] = start_point

        if "highway" in item.tags:
            node_tags["comments"] = item.tags["highway"]

        if "amenity" in item.tags:
            node_tags["r_side_description"] = item.tags["amenity"]

        if "barrier" in item.tags:
            node_tags["barrier"] = item.tags["barrier"]

        for way in ways:
            if item.id in way.nodes:

                # write way highway-type
                if "highway" in way.tags:
                    node_tags["ground_type"] = way.tags["highway"]
                    if way.tags["highway"] == "steps":
                        node_tags["is_steps"] = True
                    else:
                        node_tags["is_steps"] = False

                # write way handrail
                if "handrail" in way.tags:
                    node_tags["rail"] = way.tags["handrail"]

                # write way step-count
                if "step_count" in way.tags:
                    node_tags["steps_num"] = way.tags["step_count"]

                # write way barrier
                if "barrier" in way.tags:
                    node_tags["barrier"] = way.tags["barrier"]

                # write way name
                if "name:en" in way.tags:
                    node_tags["l_side_description"] = way.tags["name:en"]

        output.append(node_tags)

    for way in ways:
        node_ids = way.nodes
        for id in node_ids:
            node_tags = {}
            id_in_nodes = False
            for node in nodes:
                if (node.id == id) and node.tags:
                    id_in_nodes = True
            if not id_in_nodes:
                start_point = Point(0, 0, id)  # ???
                node_tags["start_point"] = start_point

                if "highway" in way.tags:
                    node_tags["ground_type"] = way.tags["highway"]
                    if way.tags["highway"] == "steps":
                        node_tags["is_steps"] = True
                    else:
                        node_tags["is_steps"] = False

                # write way handrail
                if "handrail" in way.tags:
                    node_tags["rail"] = way.tags["handrail"]

                # write way step-count
                if "step_count" in way.tags:
                    node_tags["steps_num"] = way.tags["step_count"]

                # write way barrier
                if "barrier" in way.tags:
                    node_tags["barrier"] = way.tags["barrier"]

                # write way name
                if "name:en" in way.tags:
                    node_tags["l_side_description"] = way.tags["name:en"]

                if "amenity" in way.tags:
                    node_tags["r_side_description"] = way.tags["amenity"]
            if node_tags:
                output.append(node_tags)
    return output


def writeNodesToFile(nodes, name, sheet, book):
    for i, node in enumerate(nodes):
        cell = "A" + str(i)
        print(str(node.id))
        print(sheet[cell])
        sheet[cell] = str(node.id)
    book.save(name)


def create_nodes_info(path: str):
    entities = osmToEntities(path)
    nodes = createNodes(entities)
    ways = createWays(entities)
    nodes_info = createOutputList(nodes, ways)
    return nodes_info
