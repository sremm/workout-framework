from wof.domain.types import Session, Set
from wof.repository import intensity_app

from pathlib import Path
import pytest


@pytest.fixture
def sessions_from_intensity():
    path = Path("tests", "test_data", "intensity_export.csv")
    return intensity_app.import_from_file(path)


class TestImportFromIntensity:
    def test_number_of_sessions(self, sessions_from_intensity):
        assert len(sessions_from_intensity) == 2

    def test_first_session(self, sessions_from_intensity):
        first_session = sessions_from_intensity[0]
        sets = first_session.sets
        assert sets == [Set("Single leg romanian deadlifts")]

    def test_second_session(self, sessions_from_intensity):
        second_session = sessions_from_intensity[1]
        sets = second_session.sets
        assert sets == [Set("Tuck front lever")]
