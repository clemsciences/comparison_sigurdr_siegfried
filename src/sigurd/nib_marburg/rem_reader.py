"""Read the annotated texts of the ReM corpus and train POS taggers on them."""

import pickle
from collections.abc import Iterator
from os import PathLike
from pathlib import Path
from typing import Any

from lxml import etree
from nltk.tag.sequential import BigramTagger, TrigramTagger, UnigramTagger
from nltk.tag.tnt import TnT

from sigurd import PACKAGE_DIR
from sigurd.nib_marburg.utils import (
    DATA_DIRECTORY,
    PREPROCESSED_DIRECTORY,
    get_data,
    get_root,
    make_parser,
)

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]

__all__ = [
    "ANNOTATIONS_DIRECTORY",
    "DATA_DIRECTORY",
    "PREPROCESSED_DIRECTORY",
    "read_pickle_annotations",
    "read_text_from_filename",
    "read_text_from_root",
    "read_xml_annotations",
    "save_pickle_annotations",
    "train_bigram",
    "train_tnt",
    "train_trigram",
    "train_unigram",
]

ANNOTATIONS_DIRECTORY = PACKAGE_DIR / "nib_marburg" / "annotations"
MODELS_DIRECTORY = PACKAGE_DIR / "nib_marburg"

#: A token is annotated with its normalized form, lemma, POS, generic POS, inflection,
#: inflection class and generic inflection class; punctuation is kept as a plain string.
Annotation = tuple[str | None, ...] | str | None
TrainingData = list[list[tuple[str, str]]]

_ANNOTATION_LAYERS = ("norm", "lemma", "pos", "pos_gen", "infl", "inflClass", "inflClass_gen")
_TEST_SENTENCE = ["uns", "ist", "in", "alten", "mæren", "wunders", "vil", "geseit"]


def read_text_from_filename(filename: str | PathLike[str]) -> list[list[Annotation]]:
    """Read the annotations of a CorA-XML file, sentence by sentence.

    >>> from sigurd import PACKAGE_DIR
    >>> sentences = read_text_from_filename(PACKAGE_DIR / "nib_marburg" / "M321-G1.xml")
    >>> sentences[0][0][:3]
    ('âventiure', 'âventiure', 'NA')
    """
    return read_text_from_root(get_root(filename, make_parser()))


def read_text_from_root(root: etree._Element) -> list[list[Annotation]]:
    """Read the annotations of a parsed CorA-XML document, sentence by sentence."""
    annotations: list[list[Annotation]] = [[]]
    for entry in root.findall(".//token"):
        child_diplo = entry.find("tok_dipl")
        child_anno = entry.find("tok_anno")
        if child_diplo is None or child_anno is None:
            continue
        if entry.get("type") == "token":
            annotations[-1].append(
                tuple(_layer_tag(child_anno, layer) for layer in _ANNOTATION_LAYERS)
            )
        else:
            annotations[-1].append(child_diplo.get("utf"))
            annotations.append([])
    return annotations


def _layer_tag(tok_anno: etree._Element, layer: str) -> str | None:
    child = tok_anno.find(layer)
    return None if child is None else child.get("tag")


def read_xml_annotations() -> Iterator[list[list[Annotation]]]:
    """Read the annotations of every document of the ReM corpus."""
    for root in get_data(DATA_DIRECTORY, make_parser()):
        yield read_text_from_root(root)


def save_pickle_annotations() -> None:
    """Pickle the annotations of every document of the ReM corpus in ``./annotations``."""
    for i, annotations in enumerate(read_xml_annotations(), start=1):
        with (Path("annotations") / f"annotations_{i}.pickle").open("wb") as f:
            pickle.dump(annotations, f)


def read_pickle_annotations() -> list[list[list[Annotation]]]:
    """Load the pickled annotations from :data:`ANNOTATIONS_DIRECTORY`."""
    annotations = []
    for path in sorted(ANNOTATIONS_DIRECTORY.iterdir()):
        with path.open("rb") as f:
            annotations.append(pickle.load(f))
    return annotations


def _save_and_try(tagger: Any, name: str) -> None:
    with (MODELS_DIRECTORY / f"{name}.pickle").open("wb") as f:
        pickle.dump(tagger, f)
    print(tagger.tag(_TEST_SENTENCE))


def train_tnt(data: TrainingData) -> None:
    """Train a TnT tagger, pickle it and tag a test sentence."""
    tnt_tagger = TnT()
    tnt_tagger.train(data)
    _save_and_try(tnt_tagger, "tnt")


def train_unigram(data: TrainingData) -> None:
    """Train a unigram tagger, pickle it and tag a test sentence."""
    _save_and_try(UnigramTagger(data), "unigram")


def train_bigram(data: TrainingData) -> None:
    """Train a bigram tagger, pickle it and tag a test sentence."""
    _save_and_try(BigramTagger(data), "bigram")


def train_trigram(data: TrainingData) -> None:
    """Train a trigram tagger, pickle it and tag a test sentence."""
    _save_and_try(TrigramTagger(data), "trigram")


def make_training_data(annotations: list[list[list[Annotation]]]) -> TrainingData:
    """Keep the (normalized form, POS) pairs of the annotated tokens of non-empty sentences."""
    training_data = []
    for annotation in annotations:
        for sentence in annotation:
            pairs = [(token[0], token[2]) for token in sentence if isinstance(token, tuple)]
            if pairs:
                training_data.append(pairs)
    return training_data  # type: ignore[return-value]


if __name__ == "__main__":
    training_data = make_training_data(read_pickle_annotations())
    print(training_data[0])
    train_tnt(training_data)
    train_unigram(training_data)
    train_bigram(training_data)
    train_trigram(training_data)
