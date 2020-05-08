"""

"""

import os
from lxml import etree

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


def extract_annotations(entry):
    return {child.tag: child.get("tag") for child in entry.getchildren()}


def extract_by_tag(tag, tokens):
    return [token[tag] for token in tokens if tag in token]


def get_root(filename, parser):
    tree = etree.parse(filename, parser=parser)
    return tree.getroot()


def get_data(data_directory, parser):
    for filename in os.listdir(data_directory):
        print(filename)
        if filename.endswith("xml"):
            tree = etree.parse(os.path.join(data_directory, filename), parser=parser)
            yield tree.getroot()
        else:
            print("None")
    return None
