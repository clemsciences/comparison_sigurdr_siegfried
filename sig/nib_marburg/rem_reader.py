"""

"""
import os
import pickle
from lxml import etree

from sig.nib_marburg.utils import get_data, get_root

__author__ = ["Clément Besnier <clemsciences@aol.com>", ]

DATA_DIRECTORY = "rem-corralled-20161222"
PREPROCESSED_DIRECTORY = "rem-preprocessing"

parser = etree.XMLParser(load_dtd=True, no_network=False)


def read_text_from_filename(filename):
    root = get_root(filename, parser)
    return read_text_from_filename(root)


def read_text_from_root(root):
    entries = root.findall(".//token")
    transcriptions_diplo = []
    transcriptions_anno = []
    transcriptions_anno_utf = []

    annotations = [[]]

    i = 0

    for entry in entries:
        child_diplo = entry.find("tok_dipl")
        child_anno = entry.find("tok_anno")
        transcriptions_diplo.append(child_diplo.get("utf"))
        transcriptions_anno.append(child_anno.get("trans"))
        transcriptions_anno_utf.append(child_anno.get("utf"))
        if entry.get("type") == "token":
            child_norm = child_anno.find("norm")
            child_lemma = child_anno.find("lemma")
            child_pos = child_anno.find("pos")
            child_pos_gen = child_anno.find("pos_gen")
            child_infl = child_anno.find("infl")
            child_infl_class = child_anno.find("inflClass")
            child_infl_class_gen = child_anno.find("inflClass_gen")

            annotations[i].append((
                child_norm.get("tag"),
                child_lemma.get("tag"),
                child_pos.get("tag"),
                child_pos_gen.get("tag"),
                child_infl.get("tag"),
                child_infl_class.get("tag"),
                child_infl_class_gen.get("tag")
            ))
        else:
            annotations[i].append(child_diplo.get("utf"))
            annotations.append([])

            i += 1
    return annotations


def read_annotations():
    for root in get_data(DATA_DIRECTORY, parser):
        if root is not None:
            yield read_text_from_root(root)


def save_annotations():
    i = 0
    for annotations in read_annotations():
        i += 1
        with open(os.path.join("annotations", f"annotations_{i}.pickle"), "wb") as f:
            pickle.dump(annotations, f)


save_annotations()


# print(list(read_text_from_filename("M035-N1.xml"))[:10])
