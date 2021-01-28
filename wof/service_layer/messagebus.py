from typing import Callable, Dict, List

from wof.domain import events
from wof.service_layer import handlers, unit_of_work

Handler = Callable[events.Event, unit_of_work.AbstractUnitOfWork]

HANDLERS: Dict[events.Event, List[Handler]] = {
    # events.SessionStarted: handlers...
    events.SessionsToAdd: [handlers.add_workout_sessions],
    events.SetsCompleted: [handlers.add_sets_to_workout_session],
    events.SessionsRequested: [handlers.get_sessions],
}


def handle(event: events.Event, uow: unit_of_work.AbstractUnitOfWork):
    queue = [event]
    while queue:
        event = queue.pop(0)
        for handler in HANDLERS[type(event)]:
            handler(event, uow)
            queue.extend(uow.collect_new_events())
