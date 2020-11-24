from datetime import datetime
from pathlib import Path
from typing import Dict, List, Union
from uuid import UUID

import pandas as pd
from pandas.errors import EmptyDataError
from wof.domain.model import Session, WorkoutSet
from wof.repository.base import BaseRepository


def _convert_to_sessions(data: pd.DataFrame) -> Dict[UUID, Session]:
    def _group_by_id(data: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        ids: List[str] = list(data["session_id"].unique())
        return {id: data[data["session_id"] == id] for id in ids}

    data["date"] = pd.to_datetime(data["date"])
    grouped_data = _group_by_id(data)
    results = {}
    for id_hex, group_data in grouped_data.items():
        sets = _convert_rows_to_sets(group_data)
        session_id = UUID(id_hex)
        session_date_time = group_data["date"].iloc[0]
        session = Session(sets=sets, id=session_id, date_time=session_date_time)
        results[session_id] = session
    return results


def _convert_rows_to_sets(data: pd.DataFrame) -> List[WorkoutSet]:
    def _convert_row_to_set(row: pd.Series) -> WorkoutSet:
        return WorkoutSet(
            exercise=row["exercise_name"],
            reps=row["reps"],
            weights=row["weight"],
            unit=row["unit"],
            set_number=row["set_number"],
        )

    return list(data.apply(lambda row: _convert_row_to_set(row), axis=1))


class CSVRepository(BaseRepository):
    _columns = [
        "date",
        "session_id",
        "exercise_name",
        "exercise_id",
        "reps",
        "weight",
        "set_number",
        "unit",
    ]

    def __init__(self, path: Union[Path, None] = None) -> None:
        def _load_data_if_exists(path) -> pd.DataFrame:
            if path is None or path.is_file() == False:
                df = self._create_empty_data()
            else:
                try:
                    df = pd.read_csv(path)
                except EmptyDataError:
                    df = self._create_empty_data()
            return df

        self._data_path = path
        df = _load_data_if_exists(path)
        self._all_data: Dict[UUID, Session] = _convert_to_sessions(df)

    def _create_empty_data(self) -> pd.DataFrame:
        return pd.DataFrame(columns=self._columns)

    def add(self, sessions: List[Session]) -> None:
        session_by_id = {x.id: x for x in sessions}
        self._all_data.update(session_by_id)
        self.committed = False

    def get(self, ids: List[UUID]) -> List[Session]:
        return [self._all_data[id] for id in ids]

    def list(self) -> List[Session]:
        return list(self._all_data.values())

    def commit(self) -> None:
        def _initate_record() -> Dict:
            return {key: None for key in self._columns}

        def _convert_session_data() -> pd.DataFrame:
            records: List[Dict] = []
            for session in self._all_data.values():
                for cur_set in session.sets:
                    cur_record = _initate_record()
                    cur_record["date"] = session.date_time
                    cur_record["session_id"] = session.id
                    cur_record["exercise_name"] = cur_set.exercise
                    cur_record["exercise_id"] = 0  # not implemented
                    cur_record["reps"] = cur_set.reps
                    cur_record["weight"] = cur_set.weights
                    cur_record["set_number"] = cur_set.set_number
                    cur_record["unit"] = cur_set.unit
                    records.append(cur_record)
            return pd.DataFrame.from_records(records)

        df = _convert_session_data()
        df.to_csv(self._data_path, index=False)
        self.committed = True
