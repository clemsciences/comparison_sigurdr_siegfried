"""Catalog of the texts bundled with the package, as plain text or structured data."""

from collections.abc import Callable
from dataclasses import dataclass
from functools import cache

from sigurd.nib_augsburg.nib_reader import extract_text_from_html
from sigurd.nib_augsburg.nib_reformat import extract_text
from sigurd.nib_augsburg.nib_retrieval import MAIN_LINKS
from sigurd.nib_marburg.utils import PREPROCESSED_DIRECTORY

__all__ = ["TEXTS", "Text", "get_text"]

#: Chapters (*âventiuren*), made of lines, made of half-lines.
Structure = list[list[list[str]]]


@dataclass(frozen=True)
class Text:
    """A text bundled with the package."""

    id: str
    title: str
    source: str
    load: Callable[[], str | Structure]

    def as_plain_text(self) -> str:
        """Render the text, chapters being separated by a blank line and half-lines by `` | ``."""
        content = self.load()
        if isinstance(content, str):
            return content
        return (
            "\n\n".join(
                "\n".join(" | ".join(half_line.strip() for half_line in line) for line in chapter)
                for chapter in content
            )
            + "\n"
        )

    def as_data(self) -> str | Structure:
        """Return the text as structured data if it has a structure, as a string otherwise."""
        return self.load()


@cache
def _augsburg_pages() -> dict[str, list[list[list[str]]]]:
    return {
        link: [chapter for chapter in map(extract_text, pages) if chapter]
        for link, pages in extract_text_from_html(MAIN_LINKS).items()
    }


def _augsburg(manuscript: str) -> Callable[[], Structure]:
    link = next(link for link in MAIN_LINKS if link.endswith(f"nib_{manuscript}_00.html"))
    return lambda: _augsburg_pages()[link]


def _rem(filename: str) -> Callable[[], str]:
    return lambda: (PREPROCESSED_DIRECTORY / filename).read_text(encoding="utf-8")


_AUGSBURG = "Bibliotheca Augustana, https://www.hs-augsburg.de/~harsch/germanica/Chronologie/12Jh/Nibelungen"
_REM = "Referenzkorpus Mittelhochdeutsch (CC BY-SA 4.0), https://www.linguistics.rub.de/rem/"

TEXTS: dict[str, Text] = {
    text.id: text
    for text in [
        Text("nib-a", "Nibelungenlied, manuscript A", _AUGSBURG, _augsburg("a")),
        Text("nib-b", "Nibelungenlied, manuscript B", _AUGSBURG, _augsburg("b")),
        Text("nib-c", "Nibelungenlied, manuscript C", _AUGSBURG, _augsburg("c")),
        Text("nib-n", "Nibelungenlied, manuscript n", _AUGSBURG, _augsburg("n")),
        Text(
            "rem-m321-diplomatic",
            "Nibelungenlied M321, diplomatic transcription",
            _REM,
            _rem("text_diplo"),
        ),
        Text(
            "rem-m321-annotated",
            "Nibelungenlied M321, annotated transcription",
            _REM,
            _rem("text_anno_utf"),
        ),
        Text(
            "rem-m321-normalized", "Nibelungenlied M321, normalized", _REM, _rem("text_normalized")
        ),
        Text("rem-m321-lemmatized", "Nibelungenlied M321, lemmatized", _REM, _rem("text_lemma")),
    ]
}


def get_text(text_id: str) -> Text:
    """Get a bundled text by its identifier.

    >>> get_text("nib-c").as_plain_text().splitlines()[0]
    'UNS IST> In alten | mæren wnders vil geseit'

    Raises:
        KeyError: if no text has this identifier.
    """
    try:
        return TEXTS[text_id]
    except KeyError:
        raise KeyError(f"Unknown text {text_id!r}, choose among: {', '.join(TEXTS)}") from None
