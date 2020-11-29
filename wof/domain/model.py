from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import Union, List

from datetime import datetime
from uuid import uuid4


@dataclass
class Exercise:
    """
    Descriptor for an exercise
    Has a unique id, but as with good childern, can have many names
    """

    id: int
    names: List[str]


@dataclass
class WorkoutSet:
    """ Class to define a workout set """

    exercise: Union[str, List[str]] = "name"
    reps: Union[int, List[int]] = 0
    weights: Union[float, List[float]] = 0
    unit: str = "kg"
    set_number: int = 0  # used in Intensity app as "Set"

    def __len__(self) -> int:
        if type(self.exercise) == list:
            return len(self.exercise)
        elif type(self.exercise) == str:
            return 1
        else:
            raise TypeError(f"Unexpected type for exercise: {type(self.exercise)}")


def uuid4_as_str(*args) -> str:
    return str(uuid4(*args))


@dataclass
class WorkoutSession:
    """ Class for keeping track of session data """

    sets: List[WorkoutSet] = field(default_factory=list)
    id: str = field(default_factory=uuid4_as_str)
    date_time: datetime = field(default_factory=datetime.now)

    def add_sets(self, sets: List[WorkoutSet]) -> None:
        self.sets.extend(sets)

    def __len__(self) -> int:
        return len(self.sets)
