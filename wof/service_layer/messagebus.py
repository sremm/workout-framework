from wof.domain import events
from typing import Callable, Dict, List


def send_many_sets_added_notification():
    pass


HANDLERS: Dict[events.Event, List[Callable]] = {
    events.ManySetsAddedToWorkoutSession: [send_many_sets_added_notification]
}


def handle(event: events.Event):
    for handler in HANDLERS[type(event)]:
        handler(event)
