import pickle
from pathlib import Path

import pytest

from sigurd.nib_marburg import utils
from sigurd.nib_marburg.compare_texts import DEFAULT_FILENAME, build_texts
from sigurd.nib_marburg.mhg_lemmatizer import read_lemma_to_forms


def test_save_and_read_mapping_round_trip(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(utils, "PREPROCESSED_DIRECTORY", tmp_path)
    mapping = utils.merge_mappings([{"lieben": {"liebe"}}, {"lieben": {"liebte"}, "leit": set()}])

    utils.save_mapping(mapping, "out.csv", "out.pickle")

    read = utils.read_mapping("out.csv")
    assert sorted(read["lieben"]) == ["liebe", "liebte"]
    assert read["leit"] == []
    with (tmp_path / "out.pickle").open("rb") as f:
        assert pickle.load(f) == mapping


def test_read_lemma_to_forms_keeps_first_form() -> None:
    forms = read_lemma_to_forms()
    assert sorted(forms["17"]) == ["--", "17"]


def test_build_texts_writes_every_layer(tmp_path: Path) -> None:
    build_texts(utils.get_root(DEFAULT_FILENAME, utils.make_parser()), tmp_path)

    names = {"text_diplo", "text_anno", "text_anno_utf", "text_normalized", "text_lemma"}
    assert {p.name for p in tmp_path.iterdir()} == names
    bundled = utils.PREPROCESSED_DIRECTORY / "text_lemma"
    assert (tmp_path / "text_lemma").read_text(encoding="utf-8") == bundled.read_text(
        encoding="utf-8"
    )
