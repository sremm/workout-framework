from wof.domain.model import Session
from wof.domain.model import Set


def test_add_sets_to_session():
    session = Session()
    sets = [Set(), Set()]
    session.add_sets(sets)
    assert len(session) == 2


def test_create_set_with_multiple_exercises():
    a_set = Set(
        exercise=["first", "second"],
    )
    assert len(a_set) == 2