from pathlib import Path
from typing import Dict, List, Union
from uuid import UUID

import pandas as pd
from wof.domain.model import Session
from wof.repository.base import BaseRepository


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
        self._data_path = path
        if path is None or path.is_file() == False:
            self._raw_data = self._create_empty_data()
        else:
            try:
                self._raw_data = pd.read_csv(path)
            except pd.errors.EmptyDataError:
                self._raw_data = self._create_empty_data()
        self._in_memory_data: Dict[UUID, Session] = {}

    def _create_empty_data(self) -> pd.DataFrame:
        return pd.DataFrame(columns=self._columns)

    def add(self, sessions: List[Session]) -> None:
        session_by_id = {x.id: x for x in sessions}
        self._in_memory_data.update(session_by_id)

    def get(self, ids: List[UUID]) -> List[Session]:
        return [self._in_memory_data[id] for id in ids]

    def list(self) -> List[Session]:
        return list(self._in_memory_data.values())

    def save(self) -> None:
        pass
