from io import BytesIO
from typing import Any, Dict, List, Optional

from pydantic import BaseModel
from wof.domain.model import DateTimeRange, WorkoutSession, WorkoutSet


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


class GetWorkoutSessionSummary(Command):
    date_range: DateTimeRange


class ImportSessionsFromIntensityData(Command):
    data: BytesIO

    class Config:
        arbitrary_types_allowed = True


class ImportSessionsFromPolarData(Command):
    data: List[Dict]


class ImportSessionsFromMergedPolarAndIntensityData(Command):
    polar_data: List[Dict]
    intensity_data: BytesIO

    class Config:
        arbitrary_types_allowed = True
