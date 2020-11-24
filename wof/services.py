from typing import List

from wof.domain.model import Session
from wof.repository.base import BaseRepository


def allocate_in_batch(sessions: List[Session], repo: BaseRepository) -> None:
    repo.add(sessions)
    repo.commit()
