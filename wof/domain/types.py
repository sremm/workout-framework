from dataclasses import dataclass
from typing import Union, List


@dataclass
class Set:
    """ Class to define a workout set """

    excercise: Union[str, List[str]]


@dataclass
class Session:
    """ Class for keeping track of session data"""

    id: int
    sets: List[Set]