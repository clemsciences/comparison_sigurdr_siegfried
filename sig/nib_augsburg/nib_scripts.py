"""

"""

import sig.nib_augsburg.nib_reader as reader
import sig.nib_augsburg.nib_retrieval as retrieval
import sig.nib_augsburg.nib_reformat as reformat


__author__ = ["Clément Besnier <clemsciences@aol.com>", ]


def get_nib_html():
    """
    1

    :return:
    """
    all_links = retrieval.compute_links(retrieval.MAIN_LINKS)
    nib_texts = retrieval.retrieve_texts(all_links)
    retrieval.save_texts(nib_texts)


def get_nib_txt():
    """
    2

    :return:
    """
    retrieved_nib = reader.extract_text_from_html(retrieval.MAIN_LINKS)
    reformat.save_txt_reformat(retrieval.MAIN_LINKS, retrieved_nib)


def get_nib_tei():
    """
    3

    :return:
    """
    retrieved_texts = {}
    for main_link in retrieval.MAIN_LINKS:
        retrieved_texts[main_link] = ["\n".join(["\t".join(line) for line in txt]) for txt in reader.read_txt(main_link)]
    reformat.prepare_tei(retrieval.MAIN_LINKS, retrieved_texts)


def get_nib_tei_group_annotations():
    """

    :return:
    """
    reformat.add_structure_tags(retrieval.MAIN_LINKS[0])


if __name__ == "__main__":
    get_nib_html
    get_nib_txt()
    get_nib_tei()
    get_nib_tei_group_annotations()
