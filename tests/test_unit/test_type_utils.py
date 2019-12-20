from typing import List, Dict, Mapping, Iterable, Tuple, Set, Optional, Union

from super_mario.utils.types import is_instance_of_type


def test_is_instance_of_type_simple_types():
    assert is_instance_of_type(1, int)
    assert is_instance_of_type('abc', str)
    assert is_instance_of_type([1, 2], list)
    assert is_instance_of_type({1: 2}, dict)

    assert not is_instance_of_type(1, str)
    assert not is_instance_of_type('abc', int)
    assert not is_instance_of_type([1, 2], dict)
    assert not is_instance_of_type({1: 2}, list)


def test_is_instance_of_type_basic_typing_types():
    assert is_instance_of_type([], List)
    assert is_instance_of_type({}, Dict)
    assert is_instance_of_type({}, Mapping)
    assert is_instance_of_type([], Iterable)

    assert not is_instance_of_type([], Dict)
    assert not is_instance_of_type({}, List)
    assert not is_instance_of_type({}, Tuple)
    assert not is_instance_of_type([], Set)


def test_is_instance_of_type_typing_list_with_simple_types():
    assert is_instance_of_type([1, 2, 3], List[int])
    assert not is_instance_of_type([1, 2, 3], List[str])
    assert not is_instance_of_type([1, 2, '3'], List[str])
    assert not is_instance_of_type({1: 2}, List[str])


def test_is_instance_of_type_typing_dict_with_simple_types():
    assert is_instance_of_type({1: '1', 2: '2'}, Dict[int, str])
    assert is_instance_of_type({1: '1', 2: '2'}, Mapping[int, str])

    assert not is_instance_of_type({1: '1', 2: '2'}, Dict[str, str])
    assert not is_instance_of_type({1: '1', 2: '2'}, Dict[int, int])
    assert not is_instance_of_type([1, 2, 3, 4], Dict[int, int])


def test_is_instance_of_type_typing_with_optionals():
    assert is_instance_of_type(1, Optional[int])
    assert is_instance_of_type(None, Optional[int])
    assert is_instance_of_type(None, Optional[List[int]])

    assert is_instance_of_type([], List[Optional[int]])
    assert is_instance_of_type([1, 2], List[Optional[int]])
    assert is_instance_of_type([1, 2, None], List[Optional[int]])
    assert not is_instance_of_type([1, 2, 'None'], List[Optional[int]])

    assert is_instance_of_type(None, Optional[Dict])
    assert is_instance_of_type(None, Optional[Dict[str, Optional[int]]])
    assert is_instance_of_type({'a': 1, 'b': None}, Dict[str, Optional[int]])
    assert is_instance_of_type({1: 'a', None: 'b'}, Dict[Optional[int], str])


def test_is_instance_of_type_typing_with_unions():
    assert is_instance_of_type(1, Union[int])
    assert is_instance_of_type(1, Union[int, str])
    assert is_instance_of_type('1', Union[int, str])
    assert is_instance_of_type([], Union[List, Dict])
    assert is_instance_of_type({}, Union[List, Dict])
    assert not is_instance_of_type(set(), Union[List, Dict])
    assert not is_instance_of_type([], Union[int, str])

    assert is_instance_of_type([], List[Union[int]])
    assert is_instance_of_type([1, 2], List[Union[int, str]])
    assert is_instance_of_type([1, '2'], List[Union[int, str]])
    assert not is_instance_of_type([1, '2', None], List[Union[int, str]])

    assert is_instance_of_type({'a': 1, 'b': '2'}, Dict[str, Union[int, str]])
    assert is_instance_of_type({1: 'a', '2': 'b'}, Dict[Union[int, str], str])
