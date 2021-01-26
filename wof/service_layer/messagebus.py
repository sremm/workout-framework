from wof.domain import events
from typing import Callable, Dict, List


HANDLERS: Dict[events.Event, List[Callable]] = {}


def handle_many(events: List[events.Event]):
    for event in events:
        handle(event)


def handle(event: events.Event):
    for handler in HANDLERS[type(event)]:
        handler(event)
