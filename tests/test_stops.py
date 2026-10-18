import pytest

from sigurd.stops import MIDDLE_HIGH_GERMAN_STOPS, OLD_NORSE_STOPS


@pytest.mark.parametrize("stops", [OLD_NORSE_STOPS, MIDDLE_HIGH_GERMAN_STOPS])
def test_stops_are_clean(stops: tuple[str, ...]) -> None:
    assert len(stops) == len(set(stops))
    assert all(word and word == word.strip() and word == word.lower() for word in stops)


def test_old_norse_missing_comma_is_fixed() -> None:
    assert "meðan" in OLD_NORSE_STOPS
    assert "þegar" in OLD_NORSE_STOPS
    assert "meðanþegar" not in OLD_NORSE_STOPS
