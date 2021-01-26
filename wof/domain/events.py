from typing import List, Optional, Tuple

import datetime
from pydantic import BaseModel
from wof.domain.model import WorkoutSet


class Event(BaseModel):
    pass


class SessionStarted(Event):
    pass


class SetsCompleted(Event):
    sets: List[WorkoutSet]


class DateTimeRange(BaseModel):
    start: datetime.date
    end: datetime.date


class SessionsRequested(Event):
    date_range: Optional[DateTimeRange]


class ImportRequested(Event):
    pass


class ManySetsAddedToWorkoutSession(Event):
    """
    id of the workout session
    """

    id: str
    number_of_sets_added: int
