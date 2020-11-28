from wof.service_layer import unit_of_work


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self) -> None:
        self.commited = False

    def __enter__(self):
        pass

    def commit(self):
        self.commited = True

    def rollback(self):
        pass


def test_uow_can_add_workout_sessions():
    assert 0