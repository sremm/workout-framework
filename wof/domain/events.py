from pydantic import BaseModel


class Event(BaseModel):
    pass


class ManySetsAddedToWorkoutSession(Event):
    workout_session_id: str
    number_of_sets_added: int