from datetime import datetime
from wof.domain.model import TimeSeries, WorkoutSet
from wof.import_logic import intensity_app
from wof.import_logic import polar

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
        assert sets == [
            WorkoutSet(
                exercise="Single leg romanian deadlifts",
                reps=12,
                weights=50.0,
                unit="kg",
                set_number=2,
            )
        ]

    def test_second_session(self, sessions_from_intensity):
        second_session = sessions_from_intensity[1]
        sets = second_session.sets
        assert sets == [
            WorkoutSet(
                exercise="Tuck front lever",
                reps=15,
                weights=0.0,
                unit="kg",
                set_number=2,
            )
        ]


@pytest.fixture
def sessions_from_polar():
    path = Path("tests", "test_data", "polar")
    return polar.load_all_sessions_in_folder(path)


class TestImportFromPolar:
    def test_number_of_sessions(self, sessions_from_polar):
        number_of_sessions = len(sessions_from_polar)
        assert number_of_sessions == 2

    def test_validate_first_session(self, sessions_from_polar):
        first_session = sessions_from_polar[0]
        hr = first_session.heart_rate
        assert hr == TimeSeries(
            values=[88, 89, 90],
            time=[
                datetime.strptime("2019-06-18T18:51:59", "%Y-%m-%dT%H:%M:%S"),
                datetime.strptime("2019-06-18T18:52:00", "%Y-%m-%dT%H:%M:%S"),
                datetime.strptime("2019-06-18T18:52:01", "%Y-%m-%dT%H:%M:%S"),
            ],
            unit="bpm",
        )

    def test_validate_second_session(self, sessions_from_polar):
        first_session = sessions_from_polar[1]
        hr = first_session.heart_rate
        assert hr == TimeSeries(
            values=[91, 92, 93],
            time=[
                datetime.strptime("2020-11-30T15:40:16", "%Y-%m-%dT%H:%M:%S"),
                datetime.strptime("2020-11-30T15:40:17", "%Y-%m-%dT%H:%M:%S"),
                datetime.strptime("2020-11-30T15:40:18", "%Y-%m-%dT%H:%M:%S"),
            ],
            unit="bpm",
        )
