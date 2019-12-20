from typing import NamedTuple, Union, Optional

import pytest


@pytest.fixture
def user_namedtuple():
    class User(NamedTuple):
        id: int
        email: Union[str, bytes]
        comment: Optional[str]
    return User


@pytest.fixture
def user_object():
    class User:
        pass

    u = User()
    u.id = 11
    u.email = 'test@email.com'
    u.comment = None
    return u
