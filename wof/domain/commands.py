from typing import Dict, List, Optional
from tempfile import SpooledTemporaryFile
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


class ImportSessionsFromIntensityData(Command):
    data: SpooledTemporaryFile

class ImportSessionsFromPolarData(Command):
    data: List[Dict]

class ImportSessionsFromMergedPolarAndIntensityData(Command):
    polar_data: List[Dict]
    intensity_data: SpooledTemporaryFile