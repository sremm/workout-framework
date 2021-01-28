from typing import List, Optional

import datetime
from pydantic import BaseModel
from wof.domain.model import WorkoutSession, WorkoutSet


class Event(BaseModel):
    pass


class SessionStarted(Event):
    sets: Optional[List[WorkoutSet]] = None


class SessionsToAdd(Event):
    sessions: List[WorkoutSession]


class SetsCompleted(Event):
    session_id: str
    sets: List[WorkoutSet]


class DateTimeRange(BaseModel):
    start: datetime.date
    end: datetime.date


class SessionsRequested(Event):
    date_range: Optional[DateTimeRange]


class ImportRequested(Event):
    pass
