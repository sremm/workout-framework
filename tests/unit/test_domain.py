from wof.domain.model import Session
from wof.domain.model import Set
from wof.domain.model import Excercise


def test_add_sets_to_session():
    session = Session()
    sets = [Set(), Set()]
    session.add_sets(sets)
    assert len(session) == 2


def test_create_set_with_multiple_excercises():
    a_set = Set(
        excercises=[Excercise("first"), Excercise("second")],
    )

    assert len(a_set) == 2