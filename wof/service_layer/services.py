from typing import List

from wof.domain.model import WorkoutSession
from wof.repository.base import BaseRepository


def allocate_in_batch(
    sessions: List[WorkoutSession], repo: BaseRepository, session
) -> None:
    repo.add(sessions)
    session.commit()
