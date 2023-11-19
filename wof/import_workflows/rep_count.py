from datetime import datetime
from pathlib import Path
from tempfile import SpooledTemporaryFile
from typing import Dict, List, Union

import pandas as pd

from wof.domain.model import SessionType, WorkoutSession, WorkoutSet


def import_from_file(input: Union[SpooledTemporaryFile, Path]) -> List[WorkoutSession]:
    df = pd.read_csv(input, sep=";")
    return _convert_to_sessions(df)


def _convert_to_sessions(data: pd.DataFrame) -> List[WorkoutSession]:
    grouped_data = _group_by_workout_start(data)
    result = []
    for date, group_data in grouped_data.items():
        sets = _convert_rows_to_sets(group_data)
        start_time = datetime.strptime(date, "%Y-%m-%d %H:%M")
        stop_time = datetime.strptime(
            _get_workout_end_str(group_data), "%Y-%m-%d %H:%M"
        )
        session = WorkoutSession(
            type=SessionType(name="Strength training"),
            sets=sets,
            start_time=start_time,
            stop_time=stop_time,
            origin=["rep_count_app"],
        )
        result.append(session)
    return result


def _convert_rows_to_sets(data: pd.DataFrame) -> List[WorkoutSet]:
    def _convert_row_to_set(row: pd.Series) -> WorkoutSet:
        return WorkoutSet(
            exercise=row["Exercise"],
            reps=row["Reps"],
            weights=row["Weight"],
            unit="kg",
            set_number=0,  # no number given, could try to infer somehow
        )
        # IDEA for set_number extraction we need info from the whole session, so cannot just do it row by row

    return list(data.apply(lambda row: _convert_row_to_set(row), axis=1))


def _group_by_workout_start(data: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    dates: List[str] = list(data["Workout Start"].unique())
    return {date: data[data["Workout Start"] == date] for date in dates}


def _get_workout_end_str(data: pd.DataFrame) -> str:
    dates: List[str] = list(data["Workout End"].unique())
    assert len(dates) == 1
    return dates[0]
