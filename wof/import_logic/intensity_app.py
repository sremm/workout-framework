from pathlib import Path
from wof.domain.model import Session, WorkoutSet
from typing import Dict, List, Iterable
from datetime import datetime

import pandas as pd


def import_from_file(path: Path) -> List[Session]:
    df = _load_export_file(path)
    return _convert_to_sessions(df)


def _load_export_file(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def _convert_to_sessions(data: pd.DataFrame) -> List[Session]:
    grouped_data = _group_by_date(data)
    sessions = []
    for date, group_data in grouped_data.items():
        sets = _convert_rows_to_sets(group_data)
        date_time = datetime.strptime(date, "%Y-%m-%d")
        session = Session(sets=sets, date_time=date_time)
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
