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

    normalised = [[]]
    lemmatized = [[]]
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
            normalised[i].append(child_norm.get("tag"))
            lemmatized[i].append(child_lemma.get("tag"))
        else:
            normalised[i].append(child_diplo.get("utf"))
            normalised.append([])

            lemmatized[i].append(child_diplo.get("utf"))
            lemmatized.append([])

            i += 1

    # norms = extract_by_tag("norm", tokens)
    # print(norms[:20])
    # with codecs.open(os.path.join(PREPROCESSED_DIRECTORY, "M036-N1.xml"), "r", encoding="utf-8") as f:
    #     f.write(norms)
    print(normalised[:20])


read_text("M035-N1.xml")
