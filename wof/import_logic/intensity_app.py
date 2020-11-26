from datetime import datetime
from pathlib import Path
from tempfile import SpooledTemporaryFile
from typing import Dict, List, Union

import pandas as pd
from wof.domain.model import WorkoutSession, WorkoutSet


def import_from_file(input: Union[SpooledTemporaryFile, Path]) -> List[WorkoutSession]:
    df = pd.read_csv(input)
    return _convert_to_sessions(df)


def _convert_to_sessions(data: pd.DataFrame) -> List[WorkoutSession]:
    grouped_data = _group_by_date(data)
    sessions = []
    for date, group_data in grouped_data.items():
        sets = _convert_rows_to_sets(group_data)
        date_time = datetime.strptime(date, "%Y-%m-%d")
        session = WorkoutSession(sets=sets, date_time=date_time)
        sessions.append(session)
    return sessions


def _group_by_date(data: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    dates: List[str] = list(data["Date"].unique())
    return {date: data[data["Date"] == date] for date in dates}


def _convert_rows_to_sets(data: pd.DataFrame) -> List[WorkoutSet]:
    def _convert_row_to_set(row: pd.Series) -> WorkoutSet:
        return WorkoutSet(
            exercise=row["Exercise"],
            reps=row["Reps"],
            weights=row["Weight"],
            unit=row["Unit"],
            set_number=row["Set"],
        )

    return list(data.apply(lambda row: _convert_row_to_set(row), axis=1))
