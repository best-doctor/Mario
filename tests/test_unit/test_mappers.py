from super_mario import map_object_to_namedtuple


def test_map_object_to_namedtuple_success_case(user_object, user_namedtuple):
    actual_result = map_object_to_namedtuple(user_object, user_namedtuple)
    assert isinstance(actual_result, user_namedtuple)
    assert actual_result.email == user_object.email
