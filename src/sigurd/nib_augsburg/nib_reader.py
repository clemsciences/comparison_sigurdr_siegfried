"""Read the HTML, TXT and TEI files of the Augsburg Nibelungenlied corpus."""

from pathlib import Path

from bs4 import BeautifulSoup
from lxml import etree

from sigurd import PACKAGE_DIR
from sigurd.nib_augsburg.nib_retrieval import MAIN_LINKS

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]

__all__ = [
    "MAIN_LINKS",
    "extract_text_from_html",
    "find_occurrences_in_text",
    "get_xml_root",
    "read_annotations",
    "read_cities",
    "read_names",
    "read_peoples",
    "read_regions_and_countries",
    "read_rivers",
    "read_tei",
    "read_txt",
]

NIB_AUGSBURG_DIR = PACKAGE_DIR / "nib_augsburg"
ANNOTATIONS_DIR = NIB_AUGSBURG_DIR / "annotations"

nib_directories = ["nib_a_00", "nib_b_00", "nib_c_00", "nib_n_00"]

NAMESPACES = {"n": "http://www.tei-c.org/ns/1.0"}

#: A text is made of chapters, a chapter of lines, a line of two half-lines.
Text = list[list[list[str]]]


def _manuscript_name(main_link: str) -> str:
    """Name of the manuscript of a main link, e.g. ``nib_c``."""
    return main_link.split("/")[-1].split(".")[0][:-3]


def extract_text_from_html(main_links: list[str]) -> dict[str, list[BeautifulSoup]]:
    """Parse the bundled HTML pages of each manuscript.

    >>> texts = extract_text_from_html(MAIN_LINKS)
    >>> len(texts)
    4
    >>> len(texts[MAIN_LINKS[0]])
    39

    Args:
        main_links: links to the first page of each manuscript.

    Returns:
        For each main link, the parsed pages (the title page excluded).
    """
    retrieved_texts: dict[str, list[BeautifulSoup]] = {}
    for main_link in main_links:
        directory = NIB_AUGSBURG_DIR / main_link.split("/")[-1].split(".")[0]
        n_files = sum(1 for _ in directory.iterdir())
        retrieved_texts[main_link] = [
            BeautifulSoup((directory / f"{i}.html").read_text(encoding="utf-8"), "lxml")
            for i in range(1, n_files)
        ]
    return retrieved_texts


def read_txt(main_link: str) -> list[list[list[str]]]:
    """Read the TXT files extracted by :func:`sigurd.nib_augsburg.nib_scripts.get_nib_txt`.

    >>> len(read_txt(MAIN_LINKS[0]))  # doctest: +SKIP
    39

    Args:
        main_link: link to the first page of a manuscript.

    Returns:
        For each page, its lines split into half-lines.

    Raises:
        FileNotFoundError: if the TXT files have not been extracted yet.
    """
    directory = NIB_AUGSBURG_DIR / f"extracted_{_manuscript_name(main_link)}"
    if not directory.exists():
        raise FileNotFoundError(
            "Run sigurd.nib_augsburg.nib_scripts.extract_tei_from_html() to use current function."
        )
    n_files = sum(1 for _ in directory.iterdir())
    return [
        [
            line.split("\t")
            for line in (directory / f"{i}.txt").read_text(encoding="utf-8").split("\n")
            if line
        ]
        for i in range(n_files)
    ]


def get_xml_root(main_link: str) -> etree._Element:
    """Parse the TEI file of a manuscript.

    >>> get_xml_root(MAIN_LINKS[0]).tag
    '{http://www.tei-c.org/ns/1.0}TEI'

    Args:
        main_link: link to the first page of a manuscript.

    Returns:
        The root element of the TEI document.
    """
    parser = etree.XMLParser(load_dtd=True, no_network=True)
    filename = NIB_AUGSBURG_DIR / f"{_manuscript_name(main_link)}.xml"
    return etree.parse(filename, parser=parser).getroot()


def read_tei(main_link: str) -> Text:
    """Read the TEI file of a manuscript as nested lists of half-lines.

    >>> read_tei(MAIN_LINKS[0])[0][0]
    ['UNS IST> In alten', 'mæren wnders vil geseit']

    Args:
        main_link: link to the first page of a manuscript.

    Returns:
        Chapters, made of lines, made of half-lines.
    """
    root = get_xml_root(main_link)
    return [
        [
            [segment.text or "" for segment in line.findall(".//n:seg", namespaces=NAMESPACES)]
            for line in chapter.findall(".//n:l", namespaces=NAMESPACES)
        ]
        for chapter in root.findall(".//n:chapter", namespaces=NAMESPACES)
    ]


def read_annotations(lines: list[str]) -> dict[str, list[str]]:
    """Parse annotation lines formatted as ``<normalized form>: <attested form>...``.

    Empty lines and lines starting with ``#`` are ignored.

    >>> read_annotations(["# comment", "", "Rhein: Rin Rine"])
    {'Rhein': ['Rin', 'Rine']}

    Args:
        lines: lines of an annotation file.

    Returns:
        Attested forms by normalized form.
    """
    correct_lines = [line.split(":") for line in lines if line and not line.startswith("#")]
    return {
        place[0]: [p for p in place[1].split(" ") if p]
        for place in correct_lines
        if len(place) == 2
    }


def _read_annotation_file(filename: str) -> dict[str, list[str]]:
    path: Path = ANNOTATIONS_DIR / filename
    return read_annotations(path.read_text(encoding="utf-8").strip().splitlines())


def read_peoples() -> dict[str, list[str]]:
    """Read the annotated names of peoples.

    >>> read_peoples()['Hunnen']
    ['Hunin', 'Hunen']
    """
    return _read_annotation_file("peoples.txt")


def read_regions_and_countries() -> dict[str, list[str]]:
    """Read the annotated names of regions and countries.

    >>> read_regions_and_countries()['Island']
    ['Islande']
    """
    return _read_annotation_file("regions_and_countries.txt")


def read_rivers() -> dict[str, list[str]]:
    """Read the annotated names of rivers.

    >>> read_rivers()['Rhein']
    ['Rin', 'Rine']
    """
    return _read_annotation_file("rivers.txt")


def read_cities() -> dict[str, list[str]]:
    """Read the annotated names of cities.

    >>> read_cities()['Metz']
    ['Metzzen', 'Mezzen', 'Mezzin', 'Metzen']
    """
    return _read_annotation_file("cities.txt")


def read_names() -> dict[str, list[str]]:
    """Read the annotated names of characters.

    >>> read_names()['Siegfried']
    ['Sivrit', 'Sifrit', 'Sivriden', 'Sivride', 'Sivrides']
    """
    return _read_annotation_file("names.txt")


def find_occurrences_in_text(text: Text, researched_tokens: list[str]) -> list[str]:
    """Find occurrences of given tokens in a given text.

    Each occurrence has the following format: ``<chapter>-<line>-<half-line>-<word>``.

    >>> text = read_tei(MAIN_LINKS[0])
    >>> researched_tokens = read_rivers()["Rhone"]
    >>> find_occurrences_in_text(text, researched_tokens)
    ['20-410-1-2']

    Args:
        text: chapters, made of lines, made of half-lines.
        researched_tokens: tokens to be searched in the text.

    Returns:
        Positions of the occurrences in the text, numbered from 1.
    """
    tokens = set(researched_tokens)
    return [
        f"{i + 1}-{j + 1}-{k + 1}-{m + 1}"
        for i, chapter in enumerate(text)
        for j, line in enumerate(chapter)
        for k, half_line in enumerate(line)
        for m, token in enumerate(half_line.split(" "))
        if token in tokens
    ]
