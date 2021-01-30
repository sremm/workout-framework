from pydantic import BaseModel


class Event(BaseModel):
    pass


class SomethingHappened(Event):
    pass
