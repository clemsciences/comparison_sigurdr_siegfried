"""Pipeline remaking the Augsburg Nibelungenlied TEI corpus.

Run it with ``python -m sigurd.nib_augsburg.nib_scripts``.
"""

import sigurd.nib_augsburg.nib_reader as reader
import sigurd.nib_augsburg.nib_reformat as reformat
import sigurd.nib_augsburg.nib_retrieval as retrieval

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


def get_nib_html() -> None:
    """Step 1: download the HTML pages."""
    all_links = retrieval.compute_links(retrieval.MAIN_LINKS)
    nib_texts = retrieval.retrieve_texts(all_links)
    retrieval.save_texts(nib_texts)


def get_nib_txt() -> None:
    """Step 2: extract the verses of the HTML pages into TXT files."""
    retrieved_nib = reader.extract_text_from_html(retrieval.MAIN_LINKS)
    reformat.save_txt_reformat(retrieval.MAIN_LINKS, retrieved_nib)


def get_nib_tei() -> None:
    """Step 3: concatenate the TXT files of each manuscript."""
    retrieved_texts = {
        main_link: [
            "\n".join("\t".join(line) for line in txt) for txt in reader.read_txt(main_link)
        ]
        for main_link in retrieval.MAIN_LINKS
    }
    reformat.prepare_tei(retrieval.MAIN_LINKS, retrieved_texts)


def get_nib_tei_group_annotations() -> None:
    """Step 4: add the TEI structure tags."""
    reformat.add_structure_tags(retrieval.MAIN_LINKS[0])


def get_nib_tei_segments() -> None:
    """Step 5: print the segments of the TEI file."""
    print(reader.read_tei(retrieval.MAIN_LINKS[0]))


#: Misspelled name kept for backward compatibility.
get_nib_tei_semgents = get_nib_tei_segments


def extract_tei_from_html() -> None:
    """Run the whole pipeline but the download step."""
    get_nib_txt()
    get_nib_tei()
    get_nib_tei_group_annotations()
    get_nib_tei_segments()


if __name__ == "__main__":
    extract_tei_from_html()
