from pydantic import BaseModel


class Event(BaseModel):
    pass


class ManySetsAddedToWorkoutSession(Event):
    """
    id of the workout session
    """

    id: str
    number_of_sets_added: int