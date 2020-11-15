from dataclasses import dataclass, field
from typing import Union, List

from datetime import datetime
from uuid import uuid4
from uuid import UUID


@dataclass
class Excercise:
    """
    Descriptor for an exercise
    Has a unique id, but as with good childern, can have many names
    """

    id: int
    names: List[str]


@dataclass
class Set:
    """ Class to define a workout set """

    excercise: Union[str, List[str]]
    reps: Union[int, List[int]]
    weights: Union[float, List[float]]
    unit: str = "kg"
    set_number: int = 0  # used in Intensity app as "Set"


@dataclass
class Session:
    """ Class for keeping track of session data """

    sets: List[Set] = field(default_factory=list)
    id: UUID = field(default_factory=uuid4)
    date_time: datetime = field(default_factory=datetime.now)
