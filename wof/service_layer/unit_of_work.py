import abc
from typing import Callable

from wof import config
from wof.repository.base import BaseRepository, FakeSession, FakeRepository
from wof.repository.csv import CSVRepository, CSVSession, csv_session_factory


class AbstractUnitOfWork(abc.ABC):
    repo: BaseRepository

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self) -> None:
        # self.db_session = FakeSession()
        self.repo = FakeRepository(None)
        self.commited = False

    def __enter__(self):
        pass

    def commit(self):
        self.commited = True

    def rollback(self):
        pass


DEFAULT_SESSION_FACTORY = csv_session_factory(config.get_csv_database_path())


class CSVUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: Callable = DEFAULT_SESSION_FACTORY) -> None:
        self.session_factory = session_factory

    def __enter__(self):
        self.db_session: CSVSession = self.session_factory()
        self.repo = CSVRepository(self.db_session)

        # return super().__enter__()

    def __exit__(self, *args):
        super().__exit__()
        self.db_session.close()

    def commit(self):
        self.db_session.commit()

    def rollback(self):
        self.db_session.rollback()
