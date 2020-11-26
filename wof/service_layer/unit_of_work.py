import abc
from wof.repository.base import BaseRepository


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


DEFAULT_SESSION_FACTORY = ""


class CSVUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY) -> None:
        self.session_factory = session_factory