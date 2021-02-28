import functools
from typing import Callable, List

from wof.service_layer import unit_of_work
from wof.service_layer.messagebus import Message, handle

HandleComposed = Callable[[Message], List]


def bootstrap_handle(
    uow: unit_of_work.AbstractUnitOfWork = unit_of_work.MongoUnitOfWork,
) -> HandleComposed:
    handle_composed = functools.partial(handle, uow=uow)
    return handle_composed
