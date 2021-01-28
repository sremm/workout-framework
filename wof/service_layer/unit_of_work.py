import abc
from typing import Callable, Iterable
from wof.domain import events
from wof.adapters.mongo_db import MongoSession
from wof.service_layer import messagebus

from wof.adapters.repository import (
    BaseWorkoutSessionRepository,
    MongoDBWorkoutSessionRepository,
)


class AbstractUnitOfWork(abc.ABC):
    repo: BaseWorkoutSessionRepository

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def __enter__(self):
        raise NotImplementedError

    def commit(self):
        self._commit()

    #     self.publish_events()

    # def publish_events(self):
    #     for session in self.repo.seen:
    #         while session.events:
    #             event = session.events.pop(0)
    #             messagebus.handle(event)

    def collect_new_events(self) -> Iterable[events.Event]:
        return []

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


MONGO_SESSION_FACTORY = ""


class MongoUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: Callable = MONGO_SESSION_FACTORY) -> None:
        self.session_factory = session_factory

    def __enter__(self):
        self.db_session: MongoSession = self.session_factory()
        self.repo = MongoDBWorkoutSessionRepository(self.db_session)

    def __exit__(self, *args):
        super().__exit__()

    def _commit(self):
        self.db_session.commit()

    def rollback(self):
        self.db_session.rollback()
