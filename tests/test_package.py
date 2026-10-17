from importlib.metadata import version

import sigurd


def test_version_matches_metadata() -> None:
    assert sigurd.__version__ == version("sigurd")


def test_package_dir_holds_bundled_data() -> None:
    assert (sigurd.PACKAGE_DIR / "nib_augsburg" / "nib_c.xml").is_file()
    assert (sigurd.PACKAGE_DIR / "py.typed").is_file()
    assert str(sigurd.PACKAGE_DIR) == sigurd.PACKDIR
