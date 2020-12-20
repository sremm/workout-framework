""" Domain data models 

Series x Sets x Reps of Excercies

"""
from datetime import datetime
from typing import List, Union
from uuid import uuid4

from pydantic import BaseModel, Field


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


class WorkoutSession(BaseModel):
    """ Class for keeping track of session data """

    sets: List[WorkoutSet] = Field(default_factory=list)
    id: str = Field(default_factory=uuid4_as_str)
    start_time: datetime = Field(default_factory=datetime.now)
    stop_time: Union[None, datetime] = None
    heart_rate: Union[None, TimeSeries] = None
    # sections: BaseSection # Could have sections instead sets here

    def add_sets(self, sets: List[WorkoutSet]) -> None:
        self.sets.extend(sets)
    
    def update_heart_rate(self, data:TimeSeries) -> None:
        self.heart_rate = data

    def __len__(self) -> int:
        return len(self.sets)


# might not quite work to validate and reconstuct, don't know yet
class BaseSection(BaseModel):
    """ A baseclass for Workout Section, subclass to create a specific section """

    start_time: datetime
    end_time: datetime  # or length ? either way both can be calculated from the other


class StrengthSection(BaseSection):
    sets: List[WorkoutSet]
