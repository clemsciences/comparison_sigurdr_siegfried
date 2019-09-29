"""
Reads HTML, TXT files of Nibelungenlied corpus
"""

import os
import codecs
from typing import List

from bs4 import BeautifulSoup

__author__ = ["Clément Besnier <clemsciences@aol.com>", ]

nib_directories = ["nib_a_00", "nib_b_00", "nib_c_00", "nib_n_00"]


def extract_text_from_html(main_links: List[str]) -> dict:
    """
    From HTML files to TXT files

    :param main_links:
    :return:
    """
    retrieved_texts = {}
    for main_link in main_links:
        directory = main_link.split("/")[-1].split(".")[0]
        retrieved_texts[main_link] = []
        for i in range(len(os.listdir(directory))):
            filename = os.path.join(directory, str(i)+".html")
            with open(filename, "r") as f:
                text = f.read()
                tree = BeautifulSoup(text, "lxml")
                retrieved_texts[main_link].append(tree)
    return retrieved_texts


def read_txt(main_link: str) -> List:
    """
    TXT files to str

    :param main_link:
    :return:
    """
    retrieved_texts = []
    directory = "extracted_" + main_link.split("/")[-1].split(".")[0][:-3]
    for i in range(1, len(os.listdir(directory))):
        filename = os.path.join(directory, str(i) + ".txt")
        with codecs.open(filename, "r", encoding="utf-8") as f:
            text = f.read()
            lines = [line.split("\t") for line in text.split("\n")]
        retrieved_texts.append(lines)
    return retrieved_texts
