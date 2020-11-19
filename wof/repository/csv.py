from pathlib import Path
from typing import Dict, List, Union
from uuid import UUID

import pandas as pd
from wof.domain.types import Session
from wof.repository.base import BaseRepository


class CSVRepository(BaseRepository):
    def __init__(self, path: Union[Path, None] = None) -> None:
        self._raw_data = pd.read_csv(path) if path is not None else pd.DataFrame()
        self._in_memory_data: Dict[UUID, Session] = {}

    def add(self, sessions: List[Session]) -> None:
        session_by_id = {x.id: x for x in sessions}
        self._in_memory_data.update(session_by_id)

    def get(self, ids: List[UUID]) -> List[Session]:
        return [self._in_memory_data[id] for id in ids]
