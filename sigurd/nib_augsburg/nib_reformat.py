"""
Saves TXT and TEI files.
"""

import os
import codecs
from typing import List


__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]

nib_directories = ["nib_a_00", "nib_b_00", "nib_c_00", "nib_n_00"]


def extract_text(html_text) -> List[List[str]]:
    """

    :param html_text:
    :return:
    """
    lines = [i.text.replace("\xa0", "") for i in html_text.find("div", attrs={"class": "contentus"}).findAll("h3")]
    return [line.split("  ") for line in lines if line]


def save_txt_reformat(main_links: List[str], retrieved_texts: dict):
    """
    Save TXT files

    :param main_links:
    :param retrieved_texts:
    :return:
    """
    for main_link in main_links:
        directory = "extracted_"+main_link.split("/")[-1].split(".")[0][:-3]
        if not os.path.exists(directory):
            os.mkdir(directory)
        for i, text in enumerate(retrieved_texts[main_link]):
            filename = os.path.join(directory, str(i)+".txt")
            extracted_text = extract_text(text)
            if len(extracted_text) > 0:
                with codecs.open(filename, mode="w", encoding="utf-8") as f:
                    lines = ["\t".join(line) for line in extracted_text]
                    final_text = "\n".join(lines)
                    f.write(final_text)


def prepare_tei(main_links: List[str], retrieved_texts):
    """
    Prepare TEI (XML) files

    :param main_links:
    :param retrieved_texts:
    :return:
    """
    for main_link in main_links:
        filename = main_link.split("/")[-1].split(".")[0][:-3]+".txt"
        complete_text = "\n\n".join(retrieved_texts[main_link])
        with codecs.open(filename, mode="w", encoding="utf-8") as f:
            f.write(complete_text)


def add_structure_tags(main_link: str):
    """

    :param main_link:
    :return:
    """
    filename = main_link.split("/")[-1].split(".")[0][:-3] + ".txt"
    with codecs.open(filename, "r", encoding="utf-8") as f:
        text = f.read()
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    new_lines = ["<chapter>"]
    for line in text.split("\n"):
        parts_of_line = line.split("\t")
        new_lines.append("\t<l>\n\t\t<seg>"+"</seg>\n\t\t<seg>".join(parts_of_line) +
                         "</seg>\n\t</l>")
        if line == "":
            new_lines.append("</chapter>\n<chapter>")
    new_lines.append("</chapter>")
    with codecs.open("line_annotated_"+filename, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))


def save_tei_reformat(main_links: List[str], retrieved_texts):
    """
    Save TEI (XML) files

    :param main_links:
    :param retrieved_texts:
    :return:
    """
    for main_link in main_links:
        directory = "tei_"+main_link.split("/")[-1].split(".")[0][:-3]
        if not os.path.exists(directory):
            os.mkdir(directory)
        for i, text in enumerate(retrieved_texts[main_link]):
            filename = os.path.join(directory, str(i)+".xml")
            extracted_text = extract_text(text)
            if len(extracted_text) > 0:
                with codecs.open(filename, mode="w", encoding="utf-8") as f:
                    lines = ["\t".join(line) for line in extracted_text]
                    final_text = "\n".join(lines)
                    f.write(final_text)
