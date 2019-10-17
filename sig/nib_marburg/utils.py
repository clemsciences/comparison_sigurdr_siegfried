"""

"""

__author__ = ["Clément Besnier <clemsciences@aol.com>", ]


def extract_annotations(entry):
    return {child.tag: child.get("tag") for child in entry.getchildren()}


def extract_by_tag(tag, tokens):
    return [token[tag] for token in tokens if tag in token]
