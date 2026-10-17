"""Make preprocessed CSV files.

- from lemmata to POS tags
- from POS tags to lemmata
- normalized word to POS
"""

from collections.abc import Iterator

from sigurd.nib_marburg.utils import (
    DATA_DIRECTORY,
    PREPROCESSED_DIRECTORY,
    extract_by_tag,
    get_data,
    get_tokens,
    make_parser,
    merge_mappings,
    read_mapping,
    save_mapping,
)

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]

__all__ = [
    "DATA_DIRECTORY",
    "PREPROCESSED_DIRECTORY",
    "make_lemma_to_pos_tagger",
    "make_norm_to_pos_tagger",
    "make_pos_tagger_to_lemma",
    "read_lemmata_to_pos",
    "read_norm_to_pos_tagger",
    "read_pos_tagger",
    "save_lemmata",
    "save_norm_to_pos_tagger",
    "save_pos_tagger",
]


def make_norm_to_pos_tagger() -> Iterator[dict[str, set[str]]]:
    """For each document of the ReM corpus, map each normalized form to its POS tags."""
    for root in get_data(DATA_DIRECTORY, make_parser()):
        tokens = get_tokens(root)
        yield {
            norm: {
                token["pos"]
                for token in tokens
                if "lemma" in token and "pos" in token and token["norm"] == norm
            }
            for norm in set(extract_by_tag("norm", tokens))
        }


def make_lemma_to_pos_tagger() -> Iterator[dict[str, set[str]]]:
    """For each document of the ReM corpus, map each lemma to its POS tags."""
    for root in get_data(DATA_DIRECTORY, make_parser()):
        tokens = get_tokens(root)
        yield {
            lemma: {
                token["pos"] for token in tokens if "pos" in token and token.get("lemma") == lemma
            }
            for lemma in set(extract_by_tag("lemma", tokens))
        }


def make_pos_tagger_to_lemma() -> Iterator[dict[str, set[str]]]:
    """For each document of the ReM corpus, map each POS tag to its lemmata."""
    for root in get_data(DATA_DIRECTORY, make_parser()):
        tokens = get_tokens(root)
        yield {
            pos: {
                token["lemma"] for token in tokens if "lemma" in token and token.get("pos") == pos
            }
            for pos in set(extract_by_tag("pos", tokens))
        }


def save_norm_to_pos_tagger(norm_to_pos_taggers: Iterator[dict[str, set[str]]]) -> bool:
    """Save the merged form-to-POS mappings in the current directory."""
    save_mapping(merge_mappings(norm_to_pos_taggers), "norm_pos.csv", "tokens_pos.pickle")
    return True


def save_lemmata(lemmatas: Iterator[dict[str, set[str]]]) -> bool:
    """Save the merged lemma-to-POS mappings in the current directory."""
    save_mapping(merge_mappings(lemmatas), "lemmata_pos.csv", "lemmata_pos.pickle")
    return True


def save_pos_tagger(pos_taggers: Iterator[dict[str, set[str]]]) -> bool:
    """Save the merged POS-to-lemmata mappings in the current directory."""
    save_mapping(merge_mappings(pos_taggers), "pos_lemmata.csv", "pos_lemmata.pickle")
    return True


def read_pos_tagger() -> dict[str, list[str]]:
    """Read the bundled POS-to-lemmata mapping.

    >>> "Neckar" in read_pos_tagger()["--"]
    True
    """
    return read_mapping("pos_lemmata.csv")


def read_lemmata_to_pos() -> dict[str, list[str]]:
    """Read the bundled lemma-to-POS mapping.

    >>> read_lemmata_to_pos()["Aache"]
    ['NE']
    """
    return read_mapping("lemmata_pos.csv")


def read_norm_to_pos_tagger() -> dict[str, list[str]]:
    """Read the bundled form-to-POS mapping.

    >>> read_norm_to_pos_tagger()["*sire"]
    ['NA']
    """
    return read_mapping("norm_pos.csv")


if __name__ == "__main__":
    save_pos_tagger(make_pos_tagger_to_lemma())
    save_lemmata(make_lemma_to_pos_tagger())
    save_norm_to_pos_tagger(make_norm_to_pos_tagger())
