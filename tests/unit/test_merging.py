from datetime import datetime
from wof.domain.model import TimeSeries, WorkoutSession, WorkoutSet
from wof.import_logic.data_merging import merge_polar_and_instensity_imports


def create_timeseries_entry() -> TimeSeries:
    time = [
        datetime(2000, 1, 1, 15, 0, 0, 0),
        datetime(2000, 1, 1, 15, 0, 1, 0),
        datetime(2000, 1, 1, 15, 0, 2, 0),
    ]
    return TimeSeries(values=[1, 2, 3], time=time, unit="bpm")


class TestPolarIntensityMerge:
    def test_merge_single_session_from_both(self):
        polar_imports = [
            WorkoutSession(
                id="polar",
                start_time=datetime(2020, 1, 1, 17, 0, 0, 0),
                stop_time=datetime(2020, 1, 1, 18, 0, 0, 0),
                heart_rate=create_timeseries_entry(),
            )
        ]  # has no sets
        intensity_imports = [
            WorkoutSession(
                id="intensity",
                sets=[WorkoutSet(), WorkoutSet()],
                start_time=datetime(2020, 1, 1),
            )
        ]  # has no heart rate or stop time

        result = merge_polar_and_instensity_imports(
            polar_sessions=polar_imports, intensity_sessions=intensity_imports
        )
        assert result == [
            WorkoutSession(
                id="something",
                sets=[WorkoutSet(), WorkoutSet()],
                start_time=datetime(2020, 1, 1, 17, 0, 0, 0),
                stop_time=datetime(2020, 1, 1, 18, 0, 0, 0),
                heart_rate=create_timeseries_entry(),
            )
        ]
