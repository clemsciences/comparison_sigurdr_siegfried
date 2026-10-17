from collections.abc import Callable
from pathlib import Path

import pytest

from sigurd.nib_augsburg import nib_reader
from sigurd.nib_augsburg.nib_reader import MAIN_LINKS, read_annotations, read_txt
from sigurd.nib_augsburg.nib_retrieval import compute_links, n_pages


def test_read_txt_requires_extraction(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(nib_reader, "NIB_AUGSBURG_DIR", tmp_path)
    with pytest.raises(FileNotFoundError, match="extract_tei_from_html"):
        read_txt(MAIN_LINKS[0])


def test_compute_links_covers_every_page() -> None:
    links = compute_links(MAIN_LINKS)
    assert set(links) == set(MAIN_LINKS)
    for main_link, pages in links.items():
        assert len(pages) == n_pages + 1
        assert pages[0] == main_link


@pytest.mark.parametrize(
    "reader",
    [
        nib_reader.read_cities,
        nib_reader.read_names,
        nib_reader.read_peoples,
        nib_reader.read_regions_and_countries,
        nib_reader.read_rivers,
    ],
)
def test_annotation_files_are_well_formed(reader: Callable[[], dict[str, list[str]]]) -> None:
    annotations = reader()
    assert annotations
    assert all(key and all(form.strip() for form in forms) for key, forms in annotations.items())


def test_read_annotations_ignores_malformed_lines() -> None:
    assert read_annotations(["no colon here", "a: b: c", "Rhein: Rin  Rine "]) == {
        "Rhein": ["Rin", "Rine"]
    }
