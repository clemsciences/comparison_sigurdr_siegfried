"""
Makes preprocessed csv files:
- from lemmata to POS tags
- from POS tags to lemmata
- normalized word to POS
"""

import codecs
import os

import collections
import pickle
from lxml import etree

from sig.nib_marburg.utils import get_data, extract_by_tag, extract_annotations

__author__ = ["Clément Besnier <clemsciences@aol.com>", ]


DATA_DIRECTORY = "rem-corralled-20161222"
# DATA_DIRECTORY = "."
PREPROCESSED_DIRECTORY = "rem-preprocessing"


stringify = etree.XPath("string()")
parser = etree.XMLParser(load_dtd=True, no_network=False)


def make_norm_to_pos_tagger():
    for root in get_data(DATA_DIRECTORY, parser):
        if root is not None:
            tokens = [extract_annotations(entry) for entry in root.findall(".//tok_anno")]
            norm = extract_by_tag("norm", tokens)
            norm_set = set(norm)

            pos_to_norm = {norm: {token["pos"] for token in tokens
                                  if "lemma" in token and "pos" in token and token["norm"] == norm}
                           for norm in norm_set}
            yield pos_to_norm


def make_lemma_to_pos_tagger():
    for root in get_data(DATA_DIRECTORY, parser):
        if root is not None:
            tokens = [extract_annotations(entry) for entry in root.findall(".//tok_anno")]
            lemmata = extract_by_tag("lemma", tokens)
            lemmata_set = set(lemmata)

            pos_tags = extract_by_tag("pos", tokens)
            pos_set = set(pos_tags)

            lemmata_to_pos = {lemma: {token["pos"] for token in tokens
                                      if "lemma" in token and "pos" in token and token["lemma"] == lemma}
                              for lemma in lemmata_set}
            yield lemmata_to_pos


def make_pos_tagger_to_lemma():
    for root in get_data(DATA_DIRECTORY, parser):
        if root is not None:
            tokens = [extract_annotations(entry) for entry in root.findall(".//tok_anno")]
            pos_tags = extract_by_tag("pos", tokens)
            pos_set = set(pos_tags)

            pos_to_lemmata = {pos: {token["lemma"] for token in tokens
                                    if "lemma" in token and "pos" in token and token["pos"] == pos}
                              for pos in pos_set}
            yield pos_to_lemmata


def save_norm_to_pos_tagger(norm_to_pos_taggers):
    the_norm_to_pos_taggers = collections.defaultdict(set)
    for norm_to_pos_tagger in norm_to_pos_taggers:
        for key in norm_to_pos_tagger:
            the_norm_to_pos_taggers[key].update(norm_to_pos_tagger[key])
    words = list(the_norm_to_pos_taggers.keys())
    words = sorted(words)

    with codecs.open("norm_pos.csv", "w", encoding="utf-8") as f:  # 61312
        f.write("\n".join([word + "\t" + ";".join(the_norm_to_pos_taggers[word]) for word in words]))

    with open("tokens_pos.pickle", "wb") as f:
        pickle.dump(the_norm_to_pos_taggers, f)

    return True


def save_lemmata(lemmatas):
    the_lemmata = collections.defaultdict(set)
    for lemmata in lemmatas:
        for key in lemmata:
            the_lemmata[key].update(lemmata[key])
    words = list(the_lemmata.keys())
    words = sorted(words)

    with codecs.open("lemmata_pos.csv", "w", encoding="utf-8") as f:  # 61312
        f.write("\n".join([word + "\t" + ";".join(the_lemmata[word]) for word in words]))

    with open("lemmata_pos.pickle", "wb") as f:
        pickle.dump(the_lemmata, f)

    return True


def save_pos_tagger(pos_taggers):
    the_pos_tagger = collections.defaultdict(set)
    for pos_tagger in pos_taggers:
        for key in pos_tagger:
            the_pos_tagger[key].update(pos_tagger[key])
    poss = list(the_pos_tagger.keys())
    poss = sorted(poss)

    with codecs.open("pos_lemmata.csv", "w", encoding="utf-8") as f: # 61312
        f.write("\n".join([word+"\t"+";".join(the_pos_tagger[word]) for word in poss]))

    with open("pos_lemmata.pickle", "wb") as f:
        pickle.dump(the_pos_tagger, f)

    return True


def read_pos_tagger():
    with codecs.open(os.path.join(PREPROCESSED_DIRECTORY, "pos_lemmata.csv"), "r", encoding="utf-8") as f:
        lines = f.read().split("\n")
        return {line.split("\t")[0]: line.split("\t")[1].split(";") for line in lines}


def read_lemmata_to_pos():
    with codecs.open(os.path.join(PREPROCESSED_DIRECTORY, "lemmata_pos.csv"), "r", encoding="utf-8") as f:
        lines = f.read().split("\n")
        return {line.split("\t")[0]: line.split("\t")[1].split(";") for line in lines}


def read_norm_to_pos_tagger():
    with codecs.open(os.path.join(PREPROCESSED_DIRECTORY, "norm_pos.csv"), "r", encoding="utf-8") as f:
        lines = f.read().split("\n")
        return {line.split("\t")[0]: line.split("\t")[1].split(";") for line in lines}


if __name__ == "__main__":
    pos = make_pos_tagger_to_lemma()
    save_pos_tagger(pos)

    lemmata = make_lemma_to_pos_tagger()
    save_lemmata(lemmata)

    norm_to_pos_tagger = make_norm_to_pos_tagger()
    save_norm_to_pos_tagger(norm_to_pos_tagger)

    read_lemmata_to_pos()

    read_norm_to_pos_tagger()

    read_pos_tagger()
