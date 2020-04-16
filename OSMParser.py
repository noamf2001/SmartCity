from datetime import datetime, time
from openpyxl import load_workbook, Workbook
from osmread import parse_file, Node, Way


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


def createOutputFile(nodes, ways):
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    name = ".\\{0}-data.xlsx".format(timestamp)
    book = Workbook()
    sheet = book.active

    sheet['A1'] = "ID"; sheet['B1'] = "X-Lon"; sheet['C1'] = "Y-Lat"; sheet['I1'] = "Highway-Node"
    sheet['E1'] = "Handrail"; sheet['F1'] = "Step-Count"; sheet['G1'] = "Amenity"; sheet['H1'] = "Barrier"
    sheet['D1'] = "Highway-Way"; sheet['J1'] = "Name:en"
    sheet['K1'] = "OP"; sheet['L1'] = "OP"

    for i in range(len(nodes)):
        # write node id
        cell = "A{0}".format(i + 2)
        node = nodes[i]
        sheet[cell] = node.id

        # write node lon
        cell = "B{0}".format(i + 2)
        sheet[cell] = node.lon

        # write node lat
        cell = "C{0}".format(i + 2)
        sheet[cell] = node.lat

        # write node highway-type
        if "highway" in node.tags:
            cell = "I{0}".format(i + 2)
            sheet[cell] = node.tags["highway"]

        # write node amenity
        if "amenity" in node.tags:
            cell = "G{0}".format(i + 2)
            sheet[cell] = node.tags["amenity"]

        for way in ways:
            if node.id in way.nodes:

                # write way highway-type
                if "highway" in way.tags:
                    cell = "D{0}".format(i + 2)
                    sheet[cell] = way.tags["highway"]

                # write way handrail
                if "handrail" in way.tags:
                    cell = "E{0}".format(i + 2)
                    sheet[cell] = way.tags["handrail"]

                # write way step-count
                if "step_count" in way.tags:
                    cell = "F{0}".format(i + 2)
                    sheet[cell] = way.tags["step_count"]

                # write way barrier
                if "barrier" in way.tags:
                    cell = "H{0}".format(i + 2)
                    sheet[cell] = way.tags["barrier"]


                # write way name
                if "name:en" in way.tags:
                    cell = "J{0}".format(i + 2)
                    sheet[cell] = way.tags["name:en"]

    sheet.column_dimensions["A"].width = 11
    sheet.column_dimensions["B"].width = 11
    sheet.column_dimensions["C"].width = 11
    sheet.column_dimensions["D"].width = 13
    sheet.column_dimensions["G"].width = 14

    book.save(name)
    return name, sheet, book


def writeNodesToFile(nodes, name, sheet, book):
    for i, node in enumerate(nodes):
        cell = "A" + str(i)
        print(str(node.id))
        print(sheet[cell])
        sheet[cell] = str(node.id)
    book.save(name)

def main():
    """
    documentation!!
    """
    path = "C:\\Users\\shira\\Downloads\\map (1).osm"
    entities = osmToEntities(path)
    nodes = createNodes(entities)
    ways = createWays(entities)
    name, sheet, book = createOutputFile(nodes, ways)


if __name__ == '__main__':
    main()