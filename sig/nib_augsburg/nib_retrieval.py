"""
Retrieves Augburg's Nibelungenlied corpus from https://www.hs-augsburg.de/~harsch/germanica/Chronologie/12Jh/Nibelungen
from links to HTML files.
"""

import os
import time
import requests

MAIN_LINKS = [
    "https://www.hs-augsburg.de/~harsch/germanica/Chronologie/12Jh/Nibelungen/nib_c_00.html",
    "https://www.hs-augsburg.de/~harsch/germanica/Chronologie/12Jh/Nibelungen/nib_b_00.html",
    "https://www.hs-augsburg.de/~harsch/germanica/Chronologie/12Jh/Nibelungen/nib_a_00.html",
    "https://www.hs-augsburg.de/~harsch/germanica/Chronologie/12Jh/Nibelungen/nib_n_00.html"
]

n_pages = 39

__author__ = ["Clément Besnier <clemsciences@aol.com>", ]


def int_to_string(i):
    if 0 <= i < 10:
        return "0"+str(i)
    else:
        return str(i)


def compute_links(main_links):
    """

    :param main_links:
    :return:
    """
    links = {}
    for link in main_links:
        links[link] = []
        for i in range(n_pages+1):
            link.split("/")
            links[link].append("/".join(link.split("/")[:-1])+"/" +
                               link.split("/")[-1].split(".")[0][:-2]+int_to_string(i)+".html")
    return links


def retrieve_texts(links):
    """

    :param links:
    :return:
    """
    texts = {}
    for link in links:
        texts[link] = []
        for page_link in links[link]:
            r = requests.get(page_link)
            time.sleep(1)
            texts[link].append(r.content)
    return texts


def save_texts(texts):
    """

    :param texts:
    :return:
    """
    for main_link in MAIN_LINKS:
        directory = main_link.split("/")[-1].split(".")[0]
        if not os.path.exists(directory):
            os.mkdir(directory)
        for i, text in enumerate(texts[main_link]):
            filename = os.path.join(directory, str(i)+".html")
            with open(filename, "w") as f:
                f.write(text.replace(b"s\x8d", b"i").decode("utf-8"))
