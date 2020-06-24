"""
Reads HTML, TXT files of Nibelungenlied corpus
"""

import os
import codecs
from typing import List

from lxml import etree
from bs4 import BeautifulSoup

from sigurd import PACKDIR
from sigurd.nib_augsburg.nib_retrieval import MAIN_LINKS
from sigurd.nib_augsburg import nib_scripts

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]

nib_directories = ["nib_a_00", "nib_b_00", "nib_c_00", "nib_n_00"]

NAMESPACES = {'n': 'http://www.tei-c.org/ns/1.0'}


def extract_text_from_html(main_links: List[str]) -> dict:
    """
    From HTML files to TXT files

    >>> texts = extract_text_from_html(MAIN_LINKS)
    >>> len(texts)
    4
    >>> len(texts[MAIN_LINKS[0]])
    48

    :param main_links:
    :return:
    """
    retrieved_texts = {}
    for main_link in main_links:
        directory = os.path.join(PACKDIR, "nib_augsburg", main_link.split("/")[-1].split(".")[0])
        retrieved_texts[main_link] = []
        for i in range(len(os.listdir(directory))):
            filename = os.path.join(directory, str(i) + ".html")
            with open(filename, "r") as f:
                text = f.read()
                tree = BeautifulSoup(text, "lxml")
                retrieved_texts[main_link].append(tree)
    return retrieved_texts


def read_txt(main_link: str) -> List:
    """
    TXT files to str

    >>> read_txt(MAIN_LINKS[0])

    :param main_link:
    :return:
    """
    retrieved_texts = []
    directory = os.path.join(PACKDIR, "nib_augsburg", "extracted_" + main_link.split("/")[-1].split(".")[0][:-3])
    if not os.path.exists(directory):
        nib_scripts.extract_tei_from_html()
    for i in range(1, len(os.listdir(directory))):
        filename = os.path.join(directory, str(i) + ".txt")
        with codecs.open(filename, "r", encoding="utf-8") as f:
            text = f.read()
            lines = [line.split("\t") for line in text.split("\n")]
        retrieved_texts.append(lines)
    return retrieved_texts


def get_xml_root(main_link):
    """
    >>> get_xml_root(MAIN_LINKS[0])

    :param main_link:
    :return:
    """
    parser = etree.XMLParser(load_dtd=True, no_network=False)
    filename = main_link.split("/")[-1].split(".")[0][:-3] + ".xml"
    tree = etree.parse(os.path.join(PACKDIR, "nib_augsburg", filename),
                       parser=parser)
    return tree.getroot()


def read_tei(main_link):
    """
    >>> read_tei(MAIN_LINKS[0])[0][0]
    ['UNS IST> In alten', 'mæren wnders vil geseit']

    :param main_link:
    :return:
    """
    root = get_xml_root(main_link)
    chapters = [node for node in root.findall(".//n:chapter", namespaces=NAMESPACES)]
    # lines = [[line.text for line in chapter.findall(".//l")] for chapter in chapters]
    segments = [[[segment.text for segment in line.findall(".//n:seg", namespaces=NAMESPACES)]
                 for line in chapter.findall(".//n:l", namespaces=NAMESPACES)]
                for chapter in chapters]
    return segments


def read_annotations(lines):
    correct_lines = [line.split(":") for line in lines
                     if len(line) > 0 and not line.startswith("#")]
    formatted_lines = {place[0]: [p for p in place[1].split(" ") if p]
                       for place in correct_lines if len(place) == 2}
    return formatted_lines


def read_peoples():
    """
    >>> read_peoples()['Hunnen']
    ['Hunin', 'Hunen']

    :return:
    """
    with codecs.open(os.path.join(PACKDIR, "nib_augsburg", "annotations", "peoples.txt"),
                     encoding="utf-8") as f:
        lines = f.read().strip().split(os.linesep)
    return read_annotations(lines)


def read_regions_and_countries():
    """
    >>> read_regions_and_countries()['Island']
    ['Islande']

    :return:
    """
    with codecs.open(os.path.join(PACKDIR, "nib_augsburg", "annotations", "regions_and_countries.txt"),
                     encoding="utf-8") as f:
        lines = f.read().strip().split(os.linesep)
    return read_annotations(lines)


def read_rivers():
    """
    >>> read_rivers()['Rhein']
    ['Rin', 'Rine']

    :return:
    """
    with codecs.open(os.path.join(PACKDIR, "nib_augsburg", "annotations", "rivers.txt"),
                     encoding="utf-8") as f:
        lines = f.read().strip().split(os.linesep)
    return read_annotations(lines)


def read_cities():
    """
    >>> read_cities()['Metz']
    ['Metzzen', 'Mezzen', 'Mezzin', 'Metzen']

    :return:
    """
    with codecs.open(os.path.join(PACKDIR, "nib_augsburg", "annotations", "cities.txt"),
                     encoding="utf-8") as f:
        lines = f.read().strip().split(os.linesep)
    return read_annotations(lines)


def read_names():
    """
    >>> read_names()['Siegfried']
    ['Sivrit', 'Sifrit', 'Sivriden', 'Sivride', 'Sivrides']

    :return:
    """
    with codecs.open(os.path.join(PACKDIR, "nib_augsburg", "annotations", "names.txt"),
                     encoding="utf-8") as f:
        lines = f.read().strip().split(os.linesep)
    return read_annotations(lines)


def find_occurrences_in_text(text: List[List[List[str]]],
                             researched_tokens: List[str]) -> List[str]:
    """
    Find occurrences of given tokens in a given text.

    Each occurrence has the following format: <chapter>-<line>-<half-line>-<word>.

    >>> text = read_tei(MAIN_LINKS[0])
    >>> researched_tokens = read_rivers()["Rhone"]
    >>> find_occurrences_in_text(text, researched_tokens)
    ['31-410-1-2']

    :param text: A text is composed of chapters. A chapter is composed of lines. A line is composed of 2 half lines. A half line is a string.
    :param researched_tokens: list of tokens to be searched in the text.
    :return: list of positions in the text
    """
    researched_tokens = [token for token in researched_tokens]
    return [f"{i+1}-{j+1}-{k+1}-{l+1}" for i, chapter in enumerate(text)
            for j, line in enumerate(chapter)
            for k, half_line in enumerate(line)
            for l, token in enumerate(half_line.split(" "))
            if token in researched_tokens]
