"""Export the layers (diplomatic, annotated, normalized, lemmatized) of a CorA-XML text.

Run it with ``python -m sigurd.nib_marburg.compare_texts``.
"""

from os import PathLike
from pathlib import Path

from lxml import etree

from sigurd import PACKAGE_DIR
from sigurd.nib_marburg.utils import get_root, make_parser

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]

DEFAULT_FILENAME = PACKAGE_DIR / "nib_marburg" / "M321-G1.xml"
DEFAULT_OUTPUT_DIRECTORY = "rem-preprocessing"


def build_texts(
    root: etree._Element, output_directory: str | PathLike[str] = DEFAULT_OUTPUT_DIRECTORY
) -> None:
    """Write each layer of a parsed CorA-XML document in ``output_directory``."""
    transcriptions_diplo: list[str] = []
    transcriptions_anno: list[str] = []
    transcriptions_anno_utf: list[str] = []
    normalised: list[str] = []
    lemmatized: list[str] = []

    for entry in root.findall(".//token"):
        child_diplo = entry.find("tok_dipl")
        child_anno = entry.find("tok_anno")
        if child_diplo is None or child_anno is None:
            continue
        diplo = child_diplo.get("utf", "")
        transcriptions_diplo.append(diplo)
        transcriptions_anno.append(child_anno.get("trans", ""))
        transcriptions_anno_utf.append(child_anno.get("utf", ""))
        child_norm = child_anno.find("norm")
        child_lemma = child_anno.find("lemma")
        if entry.get("type") == "token" and child_norm is not None and child_lemma is not None:
            normalised.append(child_norm.get("tag", ""))
            lemmatized.append(child_lemma.get("tag", ""))
        else:
            normalised.extend([diplo, "\n"])
            lemmatized.extend([diplo, "\n"])

    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    layers = {
        "text_diplo": transcriptions_diplo,
        "text_anno": transcriptions_anno,
        "text_anno_utf": transcriptions_anno_utf,
        "text_normalized": normalised,
        "text_lemma": lemmatized,
    }
    for filename, tokens in layers.items():
        (output / filename).write_text(" ".join(tokens), encoding="utf-8")


if __name__ == "__main__":
    build_texts(get_root(DEFAULT_FILENAME, make_parser()))
