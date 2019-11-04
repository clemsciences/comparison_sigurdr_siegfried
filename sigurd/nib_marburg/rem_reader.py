"""

"""

import os
import pickle
from lxml import etree

from nltk.tag.tnt import TnT
from nltk.tag.sequential import UnigramTagger, BigramTagger, TrigramTagger

from sigurd import PACKDIR
from sigurd.nib_marburg.utils import get_data, get_root

__author__ = ["Clément Besnier <clemsciences@aol.com>", ]

DATA_DIRECTORY = "rem-corralled-20161222"
PREPROCESSED_DIRECTORY = "rem-preprocessing"
ANNOTATIONS_DIRECTORY = os.path.join(PACKDIR, "nib_marburg", "annotations")

parser = etree.XMLParser(load_dtd=True, no_network=False)


def read_text_from_filename(filename):
    root = get_root(filename, parser)
    return read_text_from_root(root)


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


def read_xml_annotations():
    for root in get_data(DATA_DIRECTORY, parser):
        if root is not None:
            yield read_text_from_root(root)


def save_pickle_annotations():
    i = 0
    for annotations in read_xml_annotations():
        i += 1
        with open(os.path.join("annotations", f"annotations_{i}.pickle"), "wb") as f:
            pickle.dump(annotations, f)


def read_pickle_annotations():
    annotations = []
    for filename in os.listdir(ANNOTATIONS_DIRECTORY):
        with open(os.path.join(ANNOTATIONS_DIRECTORY, filename), "rb") as f:
            annotation = pickle.load(f)
        annotations.append(annotation)
    return annotations


def train_tnt(data):
    tnt_tagger = TnT()
    tnt_tagger.train(data)
    with open(os.path.join(PACKDIR, "nib_marburg", "tnt.pickle"), "wb") as f:
        pickle.dump(tnt_tagger, f)
    res = tnt_tagger.tag("uns ist in alten mæren wunders vil geseit".split(" "))
    print(res)


def train_unigram(data):
    unigram_tagger = UnigramTagger(data)
    with open(os.path.join(PACKDIR, "nib_marburg", "unigram.pickle"), "wb") as f:
        pickle.dump(unigram_tagger, f)
    res = unigram_tagger.tag("uns ist in alten mæren wunders vil geseit".split(" "))
    print(res)


def train_bigram(data):
    bigram_tagger = BigramTagger(data)
    with open(os.path.join(PACKDIR, "nib_marburg", "bigram.pickle"), "wb") as f:
        pickle.dump(bigram_tagger, f)
    res = bigram_tagger.tag("uns ist in alten mæren wunders vil geseit".split(" "))
    print(res)


def train_trigram(data):
    trigram_tagger = TrigramTagger(data)
    with open(os.path.join(PACKDIR, "nib_marburg", "trigram.pickle"), "wb") as f:
        pickle.dump(trigram_tagger, f)
    res = trigram_tagger.tag("uns ist in alten mæren wunders vil geseit".split(" "))
    print(res)


if __name__ == "__main__":
    # save_pickle_annotations()
    pickle_annotations = read_pickle_annotations()
    training_data = [[(token[0], token[2]) for token in sentence if len(token) > 2]
                     for annotation in pickle_annotations for sentence in annotation
                     if len([(token[0], token[2]) for token in sentence if len(token) > 2]) > 0]
    print(training_data[0])
    train_tnt(training_data)
    train_unigram(training_data)
    train_bigram(training_data)
    train_trigram(training_data)
