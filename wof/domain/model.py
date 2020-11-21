from dataclasses import dataclass, field
from typing import Union, List

from datetime import datetime
from uuid import uuid4
from uuid import UUID


@dataclass
class Exercise:
    """
    Descriptor for an exercise
    Has a unique id, but as with good childern, can have many names
    """

    id: int
    names: List[str]


@dataclass
class Set:
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


@dataclass
class Session:
    """ Class for keeping track of session data """

    sets: List[Set] = field(default_factory=list)
    id: UUID = field(default_factory=uuid4)
    date_time: datetime = field(default_factory=datetime.now)

    def add_sets(self, sets: List[Set]) -> None:
        pass

    def __len__(self) -> int:
        return len(self.sets)
