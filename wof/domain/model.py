""" Domain data models 

Series x Sets x Reps of Excercies

"""
from datetime import datetime
from functools import total_ordering
from typing import List, Union
from uuid import uuid4

from bson.objectid import ObjectId
from pydantic import BaseModel, Field
from wof.domain import events
from wof.domain.events import Event


class Exercise(BaseModel):
    """
    Descriptor for an exercise
    Has a unique id, but as with good childern, can have many names
    """

    id: int
    names: List[str]


class WorkoutSet(BaseModel):
    """ Class to define a workout set """

    exercise: Union[str, List[str]] = "name"
    reps: Union[int, List[int]] = 0
    weights: Union[float, List[float]] = 0
    unit: str = "kg"
    set_number: int = 1  # used in Intensity app as "Set" # would be nice to instead have start time and length later but optional
    # order of sets could be inferred if we have start times, but for imported data we probably don't

    @property
    def has_subsets(self) -> bool:
        return type(self.exercise) == type([])

    def __len__(self) -> int:
        if type(self.exercise) == list:
            return len(self.exercise)
        elif type(self.exercise) == str:
            return 1
        else:
            raise TypeError(f"Unexpected type for exercise: {type(self.exercise)}")


class TimeSeries(BaseModel):
    values: List[Union[int, float]]
    time: List[datetime]
    unit: str


def uuid4_as_str(*args) -> str:
    return str(uuid4(*args))


def object_id_as_str(*args) -> str:
    return str(ObjectId(*args))


@total_ordering
class WorkoutSession(BaseModel):
    """ Class for keeping track of session data """

    sets: List[WorkoutSet] = Field(default_factory=list)
    id: str = Field(default_factory=object_id_as_str)
    start_time: datetime = Field(default_factory=datetime.now)
    stop_time: Union[None, datetime] = None
    heart_rate: Union[None, TimeSeries] = None
    # sections: BaseSection # Could have sections instead sets here
    version: int = 1
    events: List[Event] = Field(default_factory=list)

    def add_sets(self, sets: List[WorkoutSet]) -> None:
        self.sets.extend(sets)
        self.version += 1
        if len(sets) > 5:
            self.events.append(
                events.ManySetsAddedToWorkoutSession(
                    id=self.id, number_of_sets_added=len(sets)
                )
            )

    def update_heart_rate(self, data: TimeSeries) -> None:
        self.heart_rate = data
        self.version += 1

    def __len__(self) -> int:
        return len(self.sets)

    def __lt__(self, other) -> bool:
        return self.start_time < other.start_time

    def __eq__(self, other) -> bool:
        return super().__eq__(other)

    def __hash__(self):
        return hash((type(self), self.__dict__["id"]))


class TimeSeriesStats(BaseModel):
    mean: float
    min: float
    max: float
    std: float


class WorkoutSessionsSummary(BaseModel):
    session_ids: List[str]
    total_reps: int
    total_weight_lifted: float
    heart_rate_stats: TimeSeriesStats


# might not quite work to validate and reconstuct, don't know yet
class BaseSection(BaseModel):
    """ A baseclass for Workout Section, subclass to create a specific section """

    start_time: datetime
    end_time: datetime  # or length ? either way both can be computed from the other


class StrengthSection(BaseSection):
    sets: List[WorkoutSet]
