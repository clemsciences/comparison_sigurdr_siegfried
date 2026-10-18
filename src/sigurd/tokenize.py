"""Word tokenization of Middle High German.

The Old Norse text needs none: ``norsecorpus.reader.read_tei_words`` gives it already tokenized.
"""

import re

__all__ = ["tokenize_middle_high_german"]

_PUNCTUATION = r"""[.";,:\[\]()!&?]"""

_PATTERNS = [
    # Words hyphenated at the end of a line are joined back.
    (re.compile(r"-\n"), ""),
    # Punctuation becomes a token of its own.
    (re.compile(rf"(?<=\S)(?={_PUNCTUATION})"), " "),
    (re.compile(rf"(?<={_PUNCTUATION})(?=\S)"), " "),
]


def tokenize_middle_high_german(text: str) -> list[str]:
    r"""Split a Middle High German text into words and punctuation marks.

    Like the CLTK 0.1 tokenizer it replaces, it only splits off punctuation and breaks on
    whitespace. Marks of the transcriptions that belong to a word, like the abbreviation dash
    of ``vn–`` or the apostrophe of ``Prvnh'``, stay attached to it.

    >>> tokenize_middle_high_german("UNS IST> In alten")
    ['UNS', 'IST>', 'In', 'alten']
    >>> tokenize_middle_high_german("von frevde vn– hochgeciten")
    ['von', 'frevde', 'vn–', 'hochgeciten']
    >>> tokenize_middle_high_german("dô sprach si: \"wie tuot ir sô?\"")
    ['dô', 'sprach', 'si', ':', '"', 'wie', 'tuot', 'ir', 'sô', '?', '"']
    >>> tokenize_middle_high_german("lobe-\nbæren helden")
    ['lobebæren', 'helden']

    Args:
        text: a Middle High German text.

    Returns:
        The words and punctuation marks of the text.
    """
    for pattern, replacement in _PATTERNS:
        text = pattern.sub(replacement, text)
    return text.split()
