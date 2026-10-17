"""Retrieve the Nibelungenlied corpus of the Bibliotheca Augustana.

The corpus is hosted at https://www.hs-augsburg.de/~harsch/germanica/Chronologie/12Jh/Nibelungen
and split into one HTML page per *âventiure*.
"""

import time
from pathlib import Path

import requests

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]

MAIN_LINKS = [
    "https://www.hs-augsburg.de/~harsch/germanica/Chronologie/12Jh/Nibelungen/nib_c_00.html",
    "https://www.hs-augsburg.de/~harsch/germanica/Chronologie/12Jh/Nibelungen/nib_b_00.html",
    "https://www.hs-augsburg.de/~harsch/germanica/Chronologie/12Jh/Nibelungen/nib_a_00.html",
    "https://www.hs-augsburg.de/~harsch/germanica/Chronologie/12Jh/Nibelungen/nib_n_00.html",
]

n_pages = 39

REQUEST_TIMEOUT = 30
"""Seconds to wait for the server before giving up on a page."""


def int_to_string(i: int) -> str:
    """Format a page number on two digits.

    >>> int_to_string(12)
    '12'
    >>> int_to_string(4)
    '04'

    Args:
        i: page number.

    Returns:
        The zero-padded page number.
    """
    return f"{i:02d}" if i >= 0 else str(i)


def compute_links(main_links: list[str]) -> dict[str, list[str]]:
    """Compute the links of every page of each manuscript.

    >>> links = ['http://ok.com/machin_00.html']
    >>> compute_links(links)['http://ok.com/machin_00.html'][3]
    'http://ok.com/machin_03.html'

    Args:
        main_links: links to the first page (``*_00.html``) of each manuscript.

    Returns:
        For each main link, the links of all its pages.
    """
    links = {}
    for link in main_links:
        base, _, page = link.rpartition("/")
        stem = page.split(".")[0][:-2]
        links[link] = [f"{base}/{stem}{int_to_string(i)}.html" for i in range(n_pages + 1)]
    return links


def retrieve_texts(links: dict[str, list[str]]) -> dict[str, list[bytes]]:
    """Download every page, politely waiting one second between requests.

    Args:
        links: output of :func:`compute_links`.

    Returns:
        For each main link, the raw content of all its pages.
    """
    texts: dict[str, list[bytes]] = {}
    for link, page_links in links.items():
        texts[link] = []
        for page_link in page_links:
            response = requests.get(page_link, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            time.sleep(1)
            texts[link].append(response.content)
    return texts


def save_texts(texts: dict[str, list[bytes]]) -> None:
    """Save the downloaded pages in the current directory, one folder per manuscript.

    Args:
        texts: output of :func:`retrieve_texts`.
    """
    for main_link in MAIN_LINKS:
        directory = Path(main_link.split("/")[-1].split(".")[0])
        directory.mkdir(exist_ok=True)
        for i, text in enumerate(texts[main_link]):
            (directory / f"{i}.html").write_text(
                text.replace(b"s\x8d", b"i").decode("utf-8"), encoding="utf-8"
            )
