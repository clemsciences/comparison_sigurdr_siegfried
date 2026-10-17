# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and the project adheres to [Semantic Versioning](https://semver.org/).

## [1.3.0] - Unreleased

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
