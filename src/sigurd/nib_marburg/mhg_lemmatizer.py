"""Make preprocessed CSV files.

- lemmata to (normalized) words
- (normalized) word to lemmata
"""

import collections
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
    "make_lematizer",
    "make_lemma_to_forms",
    "read_lemma_to_forms",
    "read_lemmatizer",
    "save_lemma_to_forms",
    "save_lemmatizer",
]


def make_lemma_to_forms() -> Iterator[dict[str, set[str]]]:
    """For each document of the ReM corpus, map each lemma to its normalized forms."""
    for root in get_data(DATA_DIRECTORY, make_parser()):
        tokens = get_tokens(root)
        yield {
            lemma: {
                token["norm"] for token in tokens if "norm" in token and token.get("lemma") == lemma
            }
            for lemma in set(extract_by_tag("lemma", tokens))
        }


def make_lematizer() -> Iterator[dict[str, set[str]]]:
    """For each document of the ReM corpus, map each normalized form to its lemmata."""
    for root in get_data(DATA_DIRECTORY, make_parser()):
        normalized_to_lemma: collections.defaultdict[str, set[str]] = collections.defaultdict(set)
        for token in get_tokens(root):
            if "lemma" in token:
                normalized_to_lemma[token["norm"]].add(token["lemma"])
        yield normalized_to_lemma


def save_lemma_to_forms(lemma_to_forms: Iterator[dict[str, set[str]]]) -> bool:
    """Save the merged lemma-to-forms mappings in the current directory."""
    save_mapping(merge_mappings(lemma_to_forms), "lemma_to_forms.csv", "lemma_to_tokens.pickle")
    return True


def save_lemmatizer(lemmatizers: Iterator[dict[str, set[str]]]) -> bool:
    """Save the merged form-to-lemmata mappings in the current directory."""
    save_mapping(
        merge_mappings(lemmatizers), "lemmatizer.csv", "lemmatizers.pickle", separator="\t"
    )
    return True


def read_lemmatizer() -> dict[str, list[str]]:
    """Read the bundled form-to-lemmata mapping.

    >>> read_lemmatizer()["wunders"]
    ['wunter']
    """
    return read_mapping("lemmatizer.csv", separator="\t")


def read_lemma_to_forms() -> dict[str, list[str]]:
    """Read the bundled lemma-to-forms mapping.

    >>> read_lemma_to_forms()["Aache"]
    ['Aache']
    """
    return read_mapping("lemma_to_forms.csv")


if __name__ == "__main__":
    save_lemmatizer(make_lematizer())
    save_lemma_to_forms(make_lemma_to_forms())
