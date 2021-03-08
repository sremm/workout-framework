import logging
from functools import singledispatch
from typing import Callable, Dict, List, Union

from wof.domain import commands, events, views
from wof.service_layer import handlers, unit_of_work

Handler = Callable

Message = Union[events.Event, commands.Command]

EVENT_HANDLERS: Dict[events.Event, List[Handler]] = {
    # events.SomethingHappened: [handlers.respond_to_something,handlers.respond_also_this_way],
}  # type: ignore

COMMAND_HANDLERS: Dict[events.Event, Handler] = {
    commands.AddSessions: handlers.add_workout_sessions,
    commands.AddSetsToSession: handlers.add_sets_to_workout_session,
    commands.ImportSessionsFromIntensityData: handlers.import_intensity_data,
    commands.ImportSessionsFromPolarData: handlers.import_polar_data,
    commands.ImportSessionsFromMergedPolarAndIntensityData: handlers.merge_and_import_data,
    commands.GetWorkoutSessionSummary: views.workout_sessions_summary,
    commands.GetSessions: views.workout_sessions,
}  # type: ignore


@singledispatch
def handle_message(message, queue, uow):
    raise NotImplementedError(f"No implementation for message {message}")


@handle_message.register
def _(message: events.Event, queue, uow):  # type: ignore
    for handler in EVENT_HANDLERS[type(message)]:  # type: ignore
        try:
            logging.debug(f"Handling {message=} with {handler=}", message, handler)
            handler(message, uow=uow)
            queue.extend(uow.collect_new_events())
        except Exception:
            logging.exception(f"Exception handling {message=}", message)
            continue


@handle_message.register
def _(message: commands.Command, queue, uow):
    try:
        handler = COMMAND_HANDLERS[type(message)]  # type: ignore
        result = handler(message, uow)
        queue.extend(uow.collect_new_events())
        return result
    except Exception:
        logging.exception(f"Exception handling {message=}", message)
        raise


def handle(message: Message, uow: unit_of_work.AbstractUnitOfWork) -> List:
    results = []
    queue = [message]
    while queue:
        message = queue.pop(0)
        result = handle_message(message, queue, uow)
        if result is not None:
            results.append(result)
    return results
