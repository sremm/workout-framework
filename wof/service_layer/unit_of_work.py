import abc
from typing import Callable

from wof import config
from wof.repository.base import BaseRepository
from wof.repository.csv import csv_session_factory


class AbstractUnitOfWork(abc.ABC):
    repo: BaseRepository

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


DEFAULT_SESSION_FACTORY = csv_session_factory(config.get_csv_database_path())


class CSVUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: Callable = DEFAULT_SESSION_FACTORY) -> None:
        self.session_factory = session_factory
