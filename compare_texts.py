"""

"""

import os
import re
import codecs
from lxml import etree

data_directory = "rem-preprocessing"
filename = "M321-G1.xml"

parser = etree.XMLParser(load_dtd=True, no_network=False)
tree = etree.parse(os.path.join(filename), parser=parser)
root = tree.getroot()


def build_texts(root):
    entries = root.findall(".//token")
    transcriptions_diplo = []
    transcriptions_anno = []
    transcriptions_anno_utf = []
    normalised = []
    lemmatized = []

    for entry in entries:
        child_diplo = entry.find("tok_dipl")
        child_anno = entry.find("tok_anno")
        transcriptions_diplo.append(child_diplo.get("utf"))
        transcriptions_anno.append(child_anno.get("trans"))
        transcriptions_anno_utf.append(child_anno.get("utf"))
        if entry.get("type") == "token":
            child_norm = child_anno.find("norm")
            child_lemma = child_anno.find("lemma")
            normalised.append(child_norm.get("tag"))
            lemmatized.append(child_lemma.get("tag"))
        else:
            normalised.append(child_diplo.get("utf"))
            normalised.append("\n")
            lemmatized.append(child_diplo.get("utf"))
            lemmatized.append("\n")

    # print(" ".join(transcriptions_diplo[:100]))
    # print(" ".join(transcriptions_anno[:100]))
    # print(" ".join(transcriptions_anno_utf[:100]))
    # print(" ".join(normalised[:100]))
    # print(" ".join(lemmatized[:100]))
    with codecs.open(os.path.join(data_directory, "text_diplo"), "w", encoding="utf-8") as f:
        f.write(" ".join(transcriptions_diplo))

    with codecs.open(os.path.join(data_directory, "text_anno"), "w", encoding="utf-8") as f:
        f.write(" ".join(transcriptions_anno))

    with codecs.open(os.path.join(data_directory, "text_anno_utf"), "w", encoding="utf-8") as f:
        f.write(" ".join(transcriptions_anno_utf))

    with codecs.open(os.path.join(data_directory, "text_normalized"), "w", encoding="utf-8") as f:
        f.write(" ".join(normalised))

    with codecs.open(os.path.join(data_directory, "text_lemma"), "w", encoding="utf-8") as f:
        f.write(" ".join(lemmatized))

    for lemma in lemmatized:
        if re.match(r".*lied.*", lemma):
            print(lemma)


if __name__ == "__main__":
    build_texts(root)


