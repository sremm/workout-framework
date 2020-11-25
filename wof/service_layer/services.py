from typing import List

from wof.domain.model import WorkoutSession
from wof.repository.base import BaseRepository


def allocate_in_batch(sessions: List[WorkoutSession], repo: BaseRepository) -> None:
    repo.add(sessions)
    repo.commit()
