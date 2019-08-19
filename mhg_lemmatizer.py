"""
Makes preprocessed csv files:
- lemmata to (normalized) words
- (normalized) word to lemmata
"""


import codecs
import os

import collections
from lxml import etree


DATA_DIRECTORY = "rem-corralled-20161222"


def extract_annotations(entry):
    return {child.tag: child.get("tag") for child in entry.getchildren()}


def extract_by_tag(tag, tokens):
    return [token[tag] for token in tokens if tag in token]


stringify = etree.XPath("string()")
parser = etree.XMLParser(load_dtd=True, no_network=False)


def get_data():
    for filename in os.listdir(DATA_DIRECTORY):
        print(filename)
        if filename.endswith("xml"):
            tree = etree.parse(os.path.join(DATA_DIRECTORY, filename), parser=parser)
            yield tree.getroot()
        else:
            print("None")
    return None


def make_lemma_to_forms():
    for root in get_data():
        if root:
            tokens = [extract_annotations(entry) for entry in root.findall(".//tok_anno")]
            lemmata = extract_by_tag("lemma", tokens)
            lemmata_set = set(lemmata)
            lemma_to_normalized = {lemma: {token["norm"] for token in tokens
                                           if "norm" in token and "lemma" in token and token["lemma"] == lemma}
                                   for lemma in lemmata_set}
            yield lemma_to_normalized


def make_lematizer():
    for root in get_data():
        if root:
            tokens = [extract_annotations(entry) for entry in root.findall(".//tok_anno")]
            # lemmata = extract_by_tag("lemma", tokens)
            # lemmata_set = set(lemmata)
            normalized_to_lemma = collections.defaultdict(set)
            l = [[token["norm"], token["lemma"]] for token in tokens if "lemma" in token]
            # {token["norm"]: token["lemma"] for token in tokens if "lemma" in token}
            for norm, lemma in l:
                normalized_to_lemma[norm].add(lemma)
            yield normalized_to_lemma
            #
            # pos_tags = extract_by_tag("pos", tokens)
            #
            # pos_set = set(pos_tags)
            #
            # pos_to_lemmata = {pos: {token["lemma"] for token in tokens
            #                         if "lemma" in token and "pos" in token and token["pos"] == pos}
            #                   for pos in pos_set}
        else:
            print("no root")


def save_lemma_to_forms(lemma_to_forms):
    the_lemma_to_forms = collections.defaultdict(set)
    for ltf in lemma_to_forms:
        for key in ltf:
            the_lemma_to_forms[key].update(ltf[key])

    words = list(the_lemma_to_forms.keys())
    words = sorted(words)

    with codecs.open("lemma_to_forms.csv", "w", encoding="utf-8") as f: # 61312
        f.write("\n".join([word+"\t"+";".join(the_lemma_to_forms[word]) for word in words]))
    return True


def save_lemmatizer(lemmatizers):
    the_lemmatizer = collections.defaultdict(set)
    for lemmatizer in lemmatizers:
        for key in lemmatizer:
            the_lemmatizer[key].update(lemmatizer[key])
    words = list(the_lemmatizer.keys())
    words = sorted(words)

    with codecs.open("lemmatizer.csv", "w", encoding="utf-8") as f: # 61312
        f.write("\n".join([word+"\t"+"\t".join(the_lemmatizer[word]) for word in words]))
    return True


def read_lemmatizer():
    with codecs.open("lemmatizer.csv", "r", encoding="utf-8") as f:
        lines = f.read().split("\n")
        return {line.split("\t")[0]: line.split("\t")[1:] for line in lines}


def read_lemma_to_forms():
    with codecs.open("lemma_to_forms.csv", "r", encoding="utf-8") as f:
        lines = f.read().split("\n")
        return {line.split("\t")[0]: line.split(";")[1:] for line in lines}


if __name__ == "__main__":
    lemmatizers = make_lematizer()
    save_lemmatizer(lemmatizers)

    # lemma_to_forms = make_lemma_to_forms()
    # save_lemma_to_forms(lemma_to_forms)
