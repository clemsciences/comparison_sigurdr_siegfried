# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and the project adheres to [Semantic Versioning](https://semver.org/).

## [2.0.0] - Unreleased

### Breaking changes

- Python 3.11+ is required.
- The notebook dependencies are no longer installed by default: use `pip install "sigurd[notebooks]"`.
- `sigurd.notebooks` and `sigurd.tests` are removed; notebooks are not shipped in the wheel.
- `compare_texts` is now `sigurd.nib_marburg.compare_texts`.
- `read_txt` raises `FileNotFoundError` instead of `FileExistsError`.
- The `mhg_lemmatizer` and `mhg_pos_tagger` readers read the bundled files instead of `./rem-preprocessing`.

### Changed

- Packaging moved to `pyproject.toml` (PEP 621, PEP 639 license metadata) with the `uv_build`
  backend and a `src/` layout; `setup.py`, `MANIFEST.in`, `requirements.txt` and the makefile are gone.
- Python 3.11+ is required.
- Runtime dependencies are reduced to what the library imports (`beautifulsoup4`, `lxml`, `nltk`,
  `requests`); the notebook dependencies moved to the `notebooks` extra and the dev tools to
  dependency groups.
- The package is fully type-annotated and ships `py.typed`.
- Notebooks are no longer shipped in the wheel. `sigurd.notebooks` is removed and the
  cross-cutting notebooks moved to `notebooks/`.
- `compare_texts.py` moved to `sigurd.nib_marburg.compare_texts` and no longer parses a file at import time.
- `read_txt` raises `FileNotFoundError` instead of `FileExistsError` when the TXT files are missing.
- The `read_*` functions of `mhg_lemmatizer` and `mhg_pos_tagger` read the bundled
  `rem-preprocessing` files instead of a directory relative to the current one.
- XML parsers no longer access the network.
- Progress messages of `nib_marburg.utils.get_data` go through `logging` instead of `print`.
- A `sigurd` command (`list`, `show`, `export`, `serve`) and a Dockerfile give access to the bundled texts.
- `sigurd.stops` provides the Old Norse and Middle High German stop word lists of CLTK 0.1, removed from CLTK 1.0.
- `sigurd.tokenize.tokenize_middle_high_german` replaces the CLTK 0.1 Middle High German word tokenizer.
- The notebooks no longer use CLTK: the Völsunga saga is read, already tokenized, from `norsecorpus`
  instead of the Perseus corpus, and the Word2Vec notebook uses the gensim 4 API.
  `cltk` and `scikit-learn` are removed from the `notebooks` extra.
- `sigurd.PACKAGE_DIR` (a `pathlib.Path`) is added; `sigurd.PACKDIR` is kept for compatibility.
- `nib_scripts.get_nib_tei_segments` is added; the misspelled `get_nib_tei_semgents` remains as an alias.

### Fixed

- Annotation files were split on `os.linesep`, which broke them on Windows.
- `read_lemma_to_forms` dropped the first form of every lemma.
- The CSV readers crashed on rows without any value.
- Text files are always read and written as UTF-8, whatever the platform.
- HTTP requests have a timeout and fail on HTTP errors.
- Removed the bogus `norsecorpus` console script.

## [1.2.11]

Last release built with `setup.py`.
