from datetime import datetime
from wof.domain.model import TimeSeries, WorkoutSession, WorkoutSet
from wof.import_logic.data_merging import (
    merge_polar_and_instensity_imports,
    add_sets_from_sessions,
)


def create_timeseries_entry() -> TimeSeries:
    time = [
        datetime(2000, 1, 1, 15, 0, 0, 0),
        datetime(2000, 1, 1, 15, 0, 1, 0),
        datetime(2000, 1, 1, 15, 0, 2, 0),
    ]
    return TimeSeries(values=[1, 2, 3], time=time, unit="bpm")


def test_add_sets_from_sessions():
    base_session = WorkoutSession(
        id="sess1",
        start_time=datetime(2020, 1, 1, 17, 0, 0, 0),
        stop_time=datetime(2020, 1, 1, 18, 0, 0, 0),
        heart_rate=create_timeseries_entry(),
        origin=["a"],
    )

    sessions = [
        WorkoutSession(
            id="sess2",
            sets=[WorkoutSet()],
            start_time=datetime(2020, 1, 1),
            origin=["b"],
        ),
    ]
    result = add_sets_from_sessions(base_session, sessions_with_sets=sessions)
    assert result == WorkoutSession(
        id="sess1",
        sets=[WorkoutSet()],
        start_time=datetime(2020, 1, 1, 17, 0, 0, 0),
        stop_time=datetime(2020, 1, 1, 18, 0, 0, 0),
        heart_rate=create_timeseries_entry(),
        version=2,
        origin=["a", "b"],
    )


class TestPolarIntensityMerge:
    def test_merge_two_polar_one_intensity(self):
        polar_imports = [
            WorkoutSession(
                id="polar1",
                start_time=datetime(2020, 1, 1, 17, 0, 0, 0),
                stop_time=datetime(2020, 1, 1, 18, 0, 0, 0),
                heart_rate=create_timeseries_entry(),
                origin=["polar"],
            ),
            WorkoutSession(
                id="polar2",
                start_time=datetime(2020, 1, 2, 17, 0, 0, 0),
                stop_time=datetime(2020, 1, 2, 18, 0, 0, 0),
                heart_rate=create_timeseries_entry(),
                origin=["polar"],
            ),
        ]  # has no sets
        intensity_imports = [
            WorkoutSession(
                id="intensity",
                sets=[WorkoutSet(), WorkoutSet()],
                start_time=datetime(2020, 1, 1),
                origin=["intensity"],
            )
        ]  # has no heart rate or stop time

        result = merge_polar_and_instensity_imports(
            polar_sessions=polar_imports, intensity_sessions=intensity_imports
        )
        assert result == [
            WorkoutSession(
                id="polar1",
                sets=[WorkoutSet(), WorkoutSet()],
                start_time=datetime(2020, 1, 1, 17, 0, 0, 0),
                stop_time=datetime(2020, 1, 1, 18, 0, 0, 0),
                heart_rate=create_timeseries_entry(),
                origin=["polar", "intensity"],
                version=2,
            ),
            WorkoutSession(
                id="polar2",
                start_time=datetime(2020, 1, 2, 17, 0, 0, 0),
                stop_time=datetime(2020, 1, 2, 18, 0, 0, 0),
                heart_rate=create_timeseries_entry(),
                origin=["polar"],
            ),
        ]