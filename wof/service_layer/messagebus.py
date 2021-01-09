from wof.domain import events
from typing import Callable, Dict, List


def send_many_sets_added_notification(event: events.ManySetsAddedToWorkoutSession):
    print(
        f"Many sets ({event.number_of_sets_added}) were added to session with id: {event.id}"
    )


HANDLERS: Dict[events.Event, List[Callable]] = {
    events.ManySetsAddedToWorkoutSession: [send_many_sets_added_notification]
}


def handle_many(events: List[events.Event]):
    for event in events:
        handle(event)


def handle(event: events.Event):
    for handler in HANDLERS[type(event)]:
        handler(event)
