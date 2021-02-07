import abc
from typing import Callable, Any
from wof.adapters.mongo_db import MongoSession

from wof.adapters.repository import (
    BaseWorkoutSessionRepository,
    MongoDBWorkoutSessionRepository,
)


class AbstractUnitOfWork(abc.ABC):
    repo: BaseWorkoutSessionRepository
    db_session: Any

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def __enter__(self):
        raise NotImplementedError

    def commit(self):
        self._commit()

    def collect_new_events(self):
        for session in self.repo.seen:
            while session.events:
                yield session.events.pop(0)

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
