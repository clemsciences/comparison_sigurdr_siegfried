import json
from pathlib import Path

import pytest

from sigurd.cli import main
from sigurd.texts import TEXTS, get_text


def test_list(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["list"]) == 0
    output = capsys.readouterr().out
    assert all(text_id in output for text_id in TEXTS)


def test_show_plain_text(capsys: pytest.CaptureFixture[str]) -> None:
    main(["show", "nib-a"])
    assert capsys.readouterr().out.startswith("ns ist in alten mæren | wnders vil geseit")


def test_show_json(capsys: pytest.CaptureFixture[str]) -> None:
    main(["show", "nib-b", "--json"])
    chapters = json.loads(capsys.readouterr().out)
    assert len(chapters) == 39
    assert chapters[0][0] == ["En> Bvrgonden", "ein vil edel magedin "]


def test_show_unknown_text() -> None:
    with pytest.raises(SystemExit):
        main(["show", "edda"])
    with pytest.raises(KeyError, match="choose among"):
        get_text("edda")


def test_export(tmp_path: Path) -> None:
    main(["export", str(tmp_path), "--format", "txt"])
    names = {path.name for path in tmp_path.iterdir()}
    assert names == {f"{text_id}.txt" for text_id in TEXTS} | {"index.html"}
    assert "nib-n.txt" in (tmp_path / "index.html").read_text(encoding="utf-8")
    assert (
        (tmp_path / "rem-m321-lemmatized.txt").read_text(encoding="utf-8").startswith("âventiure")
    )
