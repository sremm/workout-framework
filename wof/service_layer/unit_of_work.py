import abc
from typing import Callable
from wof.adapters.mongo_db import MongoSession

from config import DatabaseSettings
from wof.adapters.repository import (
    BaseWorkoutSessionRepository,
    CSVWorkoutSessionRepository,
    MongoDBWorkoutSessionRepository,
)
from wof.adapters.csv import CSVSession, csv_session_factory


class AbstractUnitOfWork(abc.ABC):
    repo: BaseWorkoutSessionRepository

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def __enter__(self):
        raise NotImplementedError

    def commit(self):
        self._commit()
        self.publish_events()

    def publish_events(self):
        # for all sessions seen
        # publish raised events
        pass

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


db_settings = DatabaseSettings()
DEFAULT_SESSION_FACTORY = csv_session_factory(db_settings.csv_dataset_path)


class CSVUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: Callable = DEFAULT_SESSION_FACTORY) -> None:
        self.session_factory = session_factory

    def __enter__(self):
        self.db_session: CSVSession = self.session_factory()
        self.repo = CSVWorkoutSessionRepository(self.db_session)

        # return super().__enter__()

    def __exit__(self, *args):
        super().__exit__()

    def _commit(self):
        self.db_session.commit()

    def rollback(self):
        self.db_session.rollback()
