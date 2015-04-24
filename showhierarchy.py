"""
Pretty print the hierachy of a shapefile/fiona datasource.

Presumes shapefile/datasource has a reference to a parent id
"""
import fiona
import sys
from collections import defaultdict
import operator
import argparse
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def print_decending(id, fmt, properties, children_of_id, indent, sort_by, output_fp):
    """
    Print the line for this id, and all it's children.

    :param int id: ID of element to print
    :param string fmt: Format string to use to print
    :param dict properties: Dict of id -> dict of properties for all items
    :param dict children_of_id: Dictionary of parent -> children for all items
    :param int indent: How much to indent this line by
    :param string sort_by: What key to sort the children by when printing
    :param file-like-object output_fp: Where to write the output.

    :returns: nothing
    """
    these_properties = properties[id]
    output_string = fmt.format(**these_properties)
    output_fp.write(((" " * indent) + output_string + "\n").encode("utf8"))

    # do all the children
    children_ids = children_of_id[id]
    if sort_by:
        children_ids.sort(key=lambda _id: properties[_id][sort_by])

    for child_id in children_ids:
        print_decending(child_id, fmt, properties, children_of_id, indent + 1, sort_by, output_fp)


def print_hierarchies(input_file, id_field, parent_id_field, fmt, sort_by, output_fp):
    """
    Print all hierachies for this file.

    :param string input_file: Filename to open and use
    """
    children_of_id = defaultdict(list)
    properties_for_id = {}
    with fiona.open(input_file) as input:
        for row in input:

            if row['properties'][id_field] is None:
                continue

            properties_for_id[row['properties'][id_field]] = row['properties']
            children_of_id[row['properties'][parent_id_field]].append(row['properties'][id_field])

    # find rootid. Presumed where parentid is none or equal to id
    rootids = [id for id, properties in properties_for_id.items() if properties[parent_id_field] in (id, None)]
    if len(rootids) == 0:
        # Could not find anything
        logging.critical("Found %d possible parent objects. Should be one", len(rootids))
        return
    else:
        if sort_by:
            rootids.sort(key=lambda _id: properties[_id][sort_by])
        for rootid in rootids:
            print_decending(rootid, fmt, properties_for_id, children_of_id, 0, sort_by, output_fp)


def main():
    """Parse arguments and print the output."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--id-field', help="ID field", required=True)
    parser.add_argument('-p', '--parent-id-field', help="Parent ID field", required=True)
    parser.add_argument('-f', '--format', type=unicode, help="Output format to print", required=True)
    parser.add_argument('filename', help="Filename of input file.")

    parser.add_argument('-s', '--sort', help="Sort child by this field", required=False)

    args = parser.parse_args()

    filename = args.filename
    id_field = args.id_field
    parent_id_field = args.parent_id_field

    #fmt = u"{CODE}, osm_id={OSM_ID}, {LOC_NAME} ({INT_NAME})"

    # Err messages go to stderr
    errhandler = logging.StreamHandler(sys.stderr)
    errhandler.setLevel(logging.ERROR)
    errhandler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    logger.addHandler(errhandler)

    print_hierarchies(filename, id_field, parent_id_field, args.format, args.sort, sys.stdout)


if __name__ == '__main__':
    main()
