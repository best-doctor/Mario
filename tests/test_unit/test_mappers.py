import pytest

from super_mario import map_object_to_namedtuple
from super_mario.exceptions import ProgrammingException


def test_map_object_to_namedtuple_success_case(user_object, user_namedtuple):
    actual_result = map_object_to_namedtuple(user_object, user_namedtuple)
    assert isinstance(actual_result, user_namedtuple)
    assert actual_result.email == user_object.email


def test_map_object_to_namedtuple_raises_error_on_wrong_types(user_object, user_namedtuple):
    user_object.email = 123  # non-string
    with pytest.raises(ProgrammingException):
        actual_result = map_object_to_namedtuple(user_object, user_namedtuple)
