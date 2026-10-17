"""Helpers to read the CorA-XML files of the Referenzkorpus Mittelhochdeutsch."""

import collections
import logging
import pickle
from collections.abc import Iterable, Iterator
from os import PathLike
from pathlib import Path

from lxml import etree

from sigurd import PACKAGE_DIR

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]

logger = logging.getLogger(__name__)

#: Directory of the ReM corpus, as downloaded and uncompressed in the current directory.
DATA_DIRECTORY = "rem-corralled-20161222"

#: Bundled preprocessed files.
PREPROCESSED_DIRECTORY = PACKAGE_DIR / "nib_marburg" / "rem-preprocessing"

Token = dict[str, str]


def make_parser() -> etree.XMLParser:
    """Make an XML parser that loads local DTDs but never fetches anything over the network."""
    return etree.XMLParser(load_dtd=True, no_network=True)


def extract_annotations(entry: etree._Element) -> Token:
    """Map each annotation layer of a ``tok_anno`` element to its tag."""
    return {str(child.tag): child.get("tag", "") for child in entry}


def extract_by_tag(tag: str, tokens: Iterable[Token]) -> list[str]:
    """Collect the values of an annotation layer.

    >>> extract_by_tag("pos", [{"pos": "NA"}, {"lemma": "lieben"}, {"pos": "VVFIN"}])
    ['NA', 'VVFIN']
    """
    return [token[tag] for token in tokens if tag in token]


def get_root(filename: str | PathLike[str], parser: etree.XMLParser) -> etree._Element:
    """Parse an XML file and return its root element."""
    return etree.parse(filename, parser=parser).getroot()


def get_data(
    data_directory: str | PathLike[str], parser: etree.XMLParser
) -> Iterator[etree._Element]:
    """Parse every XML file of a directory."""
    for path in sorted(Path(data_directory).iterdir()):
        if path.suffix == ".xml":
            logger.info("Parsing %s", path)
            yield get_root(path, parser)
        else:
            logger.debug("Skipping %s", path)


def get_tokens(root: etree._Element) -> list[Token]:
    """Extract the annotations of every token of a document."""
    return [extract_annotations(entry) for entry in root.findall(".//tok_anno")]


def merge_mappings(mappings: Iterable[dict[str, set[str]]]) -> dict[str, set[str]]:
    """Merge mappings to sets by taking the union of the sets of each key.

    >>> merged = merge_mappings([{"a": {"1"}}, {"a": {"2"}, "b": {"3"}}])
    >>> sorted(merged["a"]), sorted(merged["b"])
    (['1', '2'], ['3'])
    """
    merged: collections.defaultdict[str, set[str]] = collections.defaultdict(set)
    for mapping in mappings:
        for key, values in mapping.items():
            merged[key].update(values)
    return merged


def save_mapping(
    mapping: dict[str, set[str]], csv_filename: str, pickle_filename: str, separator: str = ";"
) -> None:
    """Save a mapping as a sorted TSV file (values joined by ``separator``) and as a pickle."""
    lines = [key + "\t" + separator.join(mapping[key]) for key in sorted(mapping)]
    Path(csv_filename).write_text("\n".join(lines), encoding="utf-8")
    with Path(pickle_filename).open("wb") as f:
        pickle.dump(mapping, f)


def read_mapping(filename: str, separator: str = ";") -> dict[str, list[str]]:
    """Read a TSV file written by :func:`save_mapping` from the bundled preprocessed files.

    >>> read_mapping("lemmata_pos.csv")["Aache"]
    ['NE']
    """
    text = (PREPROCESSED_DIRECTORY / filename).read_text(encoding="utf-8")
    mapping = {}
    for line in text.split("\n"):
        key, _, values = line.partition("\t")
        mapping[key] = values.split(separator) if values else []
    return mapping
