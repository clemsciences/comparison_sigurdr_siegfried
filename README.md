[![PyPI](https://img.shields.io/pypi/v/sigurd)](https://pypi.org/project/sigurd/)
[![Python versions](https://img.shields.io/pypi/pyversions/sigurd)](https://pypi.org/project/sigurd/)
[![CI](https://github.com/clemsciences/comparison_sigurdr_siegfried/actions/workflows/ci.yml/badge.svg)](https://github.com/clemsciences/comparison_sigurdr_siegfried/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/clemsciences/comparison_sigurdr_siegfried.git/master)

# Nibelungenlied and Völsunga saga

Comparison between the *Nibelungenlied* and the *Völsunga saga*.

The name of the package is **sigurd**.

Slides and code are available at [www.clementbesnier.fr/projets/cltk_2019_graz](https://www.clementbesnier.fr/projets/cltk_2019_graz).

## Installation

```bash
pip install sigurd
```

To also install what the notebooks need (norsecorpus, gensim, Jupyter…):

```bash
pip install "sigurd[notebooks]"
```

### From a local clone

To install the `sigurd` package defined in this repository, run one of these commands from its root directory:

| Command | Installs |
| --- | --- |
| `pip install .` | the package |
| `pip install ".[notebooks]"` | the package and the notebook dependencies |
| `pip install -e .` | the package in editable mode: changes to `src/sigurd/` are used without reinstalling |
| `uv tool install .` | only the `sigurd` command, in its own isolated environment |

## Usage

```python
from sigurd.nib_augsburg.nib_reader import (
    MAIN_LINKS,
    find_occurrences_in_text,
    read_names,
    read_tei,
)

text = read_tei(MAIN_LINKS[0])  # Nibelungenlied, manuscript C
find_occurrences_in_text(text, read_names()["Siegfried"])
```

The corpora are bundled with the package, so no download is needed to read them.

## Accessing the texts

The texts are available from the command line:

| Command | Effect |
| --- | --- |
| `sigurd list` | list the identifiers of the bundled texts |
| `sigurd show nib-c` | print a text, half-lines being separated by ` \| ` |
| `sigurd show nib-c --json` | print a text as JSON: chapters > lines > half-lines |
| `sigurd export texts/` | write every text as TXT and JSON in `texts/`, with an `index.html` |
| `sigurd serve` | browse the texts on http://127.0.0.1:8000 |

| Id | Text | Source |
| --- | --- | --- |
| `nib-a`, `nib-b`, `nib-c`, `nib-n` | Nibelungenlied, manuscripts A, B, C and n | Bibliotheca Augustana |
| `rem-m321-diplomatic`, `rem-m321-annotated`, `rem-m321-normalized`, `rem-m321-lemmatized` | Nibelungenlied M321, four layers | Referenzkorpus Mittelhochdeutsch |

### With Docker

No Python needed. Build the image:

```bash
docker build -t sigurd .
```

Then:

| Command | Effect |
| --- | --- |
| `docker run --rm -p 8000:8000 sigurd` | browse the texts on http://localhost:8000 |
| `docker run --rm sigurd show nib-a > nib-a.txt` | save a single text |
| `docker run --rm -v "$PWD/texts:/out" -u "$(id -u)" sigurd export /out` | save every text in `texts/` |

## Repository layout

| Path | Content |
| --- | --- |
| `src/sigurd/nib_augsburg/` | Readers and pipeline for the Bibliotheca Augustana Nibelungenlied (manuscripts A, B, C, n) |
| `src/sigurd/nib_marburg/` | Readers, lemmatizer and POS tagger data for the Referenzkorpus Mittelhochdeutsch |
| `notebooks/` | Exploratory notebooks (the ones next to their data stay in `src/sigurd/`, they are not shipped in the wheel) |
| `presentation/` | Slides of the Graz presentation (6th November 2019) |
| `tests/` | Test suite (doctests in `src/` run too) |

## Development

The project is managed with [uv](https://docs.astral.sh/uv/).

| Command | Effect |
| --- | --- |
| `uv sync` | create `.venv` with the dev dependencies |
| `uv run pytest` | run the tests and doctests |
| `uv run ruff check` | lint |
| `uv run ruff format` | format |
| `uv run mypy` | type check |
| `uv run pre-commit install` | run the checks before each commit |
| `uv build` | build the sdist and the wheel |

Releases are published to PyPI by GitHub Actions when a `v*` tag matching the version in
`pyproject.toml` is pushed (bump it with `uv version --bump minor`).

## Origins of the data

### Völsunga saga

For Old Norse texts: https://github.com/clemsciences/old_norse_corpus and ultimately https://heimskringla.no/wiki/Main_Page.

### Bibliotheca Augustana

The Nibelungenlied manuscripts come from https://www.hs-augsburg.de/~harsch/germanica/Chronologie/12Jh/Nibelungen.

### Stop words

`sigurd.stops` holds the Old Norse (by Clément Besnier) and Middle High German (by Eleftheria
Chatziargyriou) stop word lists of [CLTK](https://github.com/cltk/cltk) 0.1.121, which CLTK 1.0
and later no longer provide.

### Referenzkorpus Mittelhochdeutsch

#### Source and license

[Main page of the project](https://www.linguistics.rub.de/rem/access/index.html)

> Klein, Thomas; Wegera, Klaus-Peter; Dipper, Stefanie; Wich-Reif, Claudia (2016). Referenzkorpus Mittelhochdeutsch (1050–1350), Version 1.0, https://www.linguistics.ruhr-uni-bochum.de/rem/. ISLRN 332-536-136-099-5.

License:

> Das Referenzkorpus Mittelhochdeutsch ist lizenziert unter einer [Creative Commons Namensnennung - Weitergabe unter gleichen Bedingungen 4.0 International Lizenz](https://creativecommons.org/licenses/by-sa/4.0/).

No change is made on the corpus. This code is intended to parse the corpus.

#### Corpus retrieval

1. Go to https://www.linguistics.rub.de/rem/access/index.html.
2. Click on "CORA-XML AKS .TAR.XZ" or "CORA-XML ALS .ZIP".
3. Click on "Herunterladen".
4. Uncompress the downloaded file in your working directory.
5. You have a folder, named **rem-corralled-20161222** (2019-09-18), with a list of XML files which are annotated texts.

## Citation

See [`CITATION.cff`](CITATION.cff).
