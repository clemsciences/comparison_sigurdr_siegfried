"""Save the Augsburg Nibelungenlied as TXT and TEI files in the current directory."""

from pathlib import Path

from bs4 import BeautifulSoup

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]

nib_directories = ["nib_a_00", "nib_b_00", "nib_c_00", "nib_n_00"]


def _manuscript_name(main_link: str) -> str:
    return main_link.split("/")[-1].split(".")[0][:-3]


def extract_text(html_text: BeautifulSoup) -> list[list[str]]:
    r"""Extract the verses of a parsed page.

    >>> page = BeautifulSoup(
    ...     '<div class="contentus"><h3>Uns ist in alten\xa0  mæren wunders vil geseit</h3></div>',
    ...     "html.parser",
    ... )
    >>> extract_text(page)
    [['Uns ist in alten', 'mæren wunders vil geseit']]

    Args:
        html_text: a page of the corpus.

    Returns:
        Lines split into half-lines.
    """
    content = html_text.find("div", attrs={"class": "contentus"})
    if content is None:
        return []
    lines = [h3.text.replace("\xa0", "") for h3 in content.find_all("h3")]
    return [line.split("  ") for line in lines if line]


def _write_pages(directory: Path, pages: list[BeautifulSoup], suffix: str) -> None:
    directory.mkdir(exist_ok=True)
    for i, page in enumerate(pages):
        extracted_text = extract_text(page)
        if extracted_text:
            (directory / f"{i}{suffix}").write_text(
                "\n".join("\t".join(line) for line in extracted_text), encoding="utf-8"
            )


def save_txt_reformat(
    main_links: list[str], retrieved_texts: dict[str, list[BeautifulSoup]]
) -> None:
    """Save the verses of each page as a TXT file, half-lines being separated by a tab.

    Args:
        main_links: links to the first page of each manuscript.
        retrieved_texts: output of :func:`sigurd.nib_augsburg.nib_reader.extract_text_from_html`.
    """
    for main_link in main_links:
        directory = Path(f"extracted_{_manuscript_name(main_link)}")
        _write_pages(directory, retrieved_texts[main_link], ".txt")


def prepare_tei(main_links: list[str], retrieved_texts: dict[str, list[str]]) -> None:
    """Concatenate the pages of each manuscript in a single TXT file, to be turned into TEI.

    Args:
        main_links: links to the first page of each manuscript.
        retrieved_texts: for each main link, the text of each page.
    """
    for main_link in main_links:
        Path(f"{_manuscript_name(main_link)}.txt").write_text(
            "\n\n".join(retrieved_texts[main_link]), encoding="utf-8"
        )


def add_structure_tags(main_link: str) -> None:
    """Wrap the text prepared by :func:`prepare_tei` in ``<chapter>``, ``<l>`` and ``<seg>`` tags.

    Args:
        main_link: link to the first page of a manuscript.
    """
    filename = f"{_manuscript_name(main_link)}.txt"
    text = Path(filename).read_text(encoding="utf-8")
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    new_lines = ["<chapter>"]
    for line in text.split("\n"):
        parts_of_line = line.split("\t")
        new_lines.append(
            "\t<l>\n\t\t<seg>" + "</seg>\n\t\t<seg>".join(parts_of_line) + "</seg>\n\t</l>"
        )
        if line == "":
            new_lines.append("</chapter>\n<chapter>")
    new_lines.append("</chapter>")
    Path(f"line_annotated_{filename}").write_text("\n".join(new_lines), encoding="utf-8")


def save_tei_reformat(
    main_links: list[str], retrieved_texts: dict[str, list[BeautifulSoup]]
) -> None:
    """Save the verses of each page as an XML file.

    Args:
        main_links: links to the first page of each manuscript.
        retrieved_texts: output of :func:`sigurd.nib_augsburg.nib_reader.extract_text_from_html`.
    """
    for main_link in main_links:
        directory = Path(f"tei_{_manuscript_name(main_link)}")
        _write_pages(directory, retrieved_texts[main_link], ".xml")
