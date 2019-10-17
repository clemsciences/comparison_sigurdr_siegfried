"""

"""


import os
import codecs

from lxml import etree
from sig.nib_marburg.utils import extract_annotations, extract_by_tag


__author__ = ["Clément Besnier <clemsciences@aol.com>", ]

DATA_DIRECTORY = "rem-corralled-20161222"
# DATA_DIRECTORY = "."
PREPROCESSED_DIRECTORY = "rem-preprocessing"

parser = etree.XMLParser(load_dtd=True, no_network=False)


def read_text(filename):
    tree = etree.parse(os.path.join(DATA_DIRECTORY, filename), parser=parser)
    root = tree.getroot()
    # tokens = [extract_annotations(entry) for entry in root.findall(".//tok_anno")]

    entries = root.findall(".//token")

    transcriptions_diplo = []
    transcriptions_anno = []
    transcriptions_anno_utf = []

    annotations = [[]]

    # normalised = [[]]
    # lemmatized = [[]]
    # pos = [[]]
    # pos_gen = [[]]
    # infl = [[]]
    # infl_class = [[]]
    # infl_class_gen = [[]]

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

            # normalised[i].append(child_norm.get("tag"))
            # lemmatized[i].append(child_lemma.get("tag"))
            # pos[i].append(child_pos.get("tag"))
            # pos_gen[i].append(child_pos_gen.get("tag"))
            # infl[i].append(child_infl.get("tag"))
            # infl_class[i].append(child_infl_class.get("tag"))
            # infl_class_gen[i].append(child_infl_class_gen.get("tag"))

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
            # normalised[i].append(child_diplo.get("utf"))
            # normalised.append([])
            #
            # lemmatized[i].append(child_diplo.get("utf"))
            # lemmatized.append([])
            #
            # pos[i].append(child_diplo.get("utf"))
            # pos.append([])
            #
            # pos_gen[i].append(child_diplo.get("utf"))
            # pos_gen.append([])
            #
            # infl[i].append(child_diplo.get("utf"))
            # infl.append([])
            #
            # infl_class[i].append(child_diplo.get("utf"))
            # infl_class.append([])
            #
            # infl_class_gen[i].append(child_diplo.get("utf"))
            # infl_class_gen.append([])

            annotations[i].append(child_diplo.get("utf"))
            annotations.append([])

            i += 1

    # norms = extract_by_tag("norm", tokens)
    # print(norms[:20])
    # with codecs.open(os.path.join(PREPROCESSED_DIRECTORY, "M036-N1.xml"), "r", encoding="utf-8") as f:
    #     f.write(norms)
    # print(normalised[:20])
    # print(pos[:20])
    # print(pos_gen[:20])
    # print(infl[:20])
    # print(infl_class[:20])
    # print(infl_class_gen[:20])

    # return zip(normalised, pos, pos_gen, infl, infl_class, infl_class_gen)
    return annotations


def annotation_text(filename):
    pass


print(list(read_text("M035-N1.xml"))[:10])
