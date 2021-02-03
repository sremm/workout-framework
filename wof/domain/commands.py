from typing import List, Optional

from pydantic import BaseModel
from wof.domain.model import WorkoutSession, WorkoutSet, DateTimeRange


class Command(BaseModel):
    pass


class CreateSession(Command):
    sets: Optional[List[WorkoutSet]] = None


class AddSessions(Command):
    sessions: List[WorkoutSession]


class AddSetsToSession(Command):
    session_id: str
    sets: List[WorkoutSet]


class GetSessions(Command):
    date_range: Optional[DateTimeRange]


class ImportData(Command):
    pass
