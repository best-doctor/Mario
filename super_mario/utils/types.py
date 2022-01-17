from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, date
from decimal import Decimal
from typing import Any, Optional, Iterable, TYPE_CHECKING

from typing_inspect import get_origin, get_args, is_optional_type, is_union_type

from super_mario.utils.lists import flat

if TYPE_CHECKING:
    from typing import Type


def is_contains_only_basic_types(some_data: Any) -> bool:
    allowed_containers = (
        dict,
        list,
        tuple,
    )
    allowed_types = (
        int,
        float,
        str,
        datetime,
        Decimal,
        date,
    )

    if some_data is None:
        return True

    if isinstance(some_data, allowed_containers):
        if isinstance(some_data, dict):
            subitems: Iterable = flat(some_data.items())
        else:
            subitems = some_data
        return all(is_contains_only_basic_types(d) for d in subitems)
    return isinstance(some_data, allowed_types) or is_instance_of_named_tuple(some_data)


def is_instance_of_named_tuple(object_: Any) -> bool:
    return isinstance(object_, tuple) and hasattr(object_, '_fields')


def is_instance_of_type(_object: Any, required_type: Type) -> Optional[bool]:
    """
    Check if `object` is of type `required_type`.

    Works same as `isinstance`, but also has limited support of typing
    generics (such as Union, Optional, etc).

    Works on small subset of types, can fail on complex types.
    See tests (tests/tests_unit/test_type_utils.py) for examples.
    """
    type_to_check_first = required_type
    if is_optional_type(required_type) or is_union_type(required_type):
        type_to_check_first = get_args(required_type)
    try:
        return isinstance(_object, type_to_check_first)
    except TypeError:
        pass

    if is_optional_type(required_type):
        if _object is None:
            return True
        required_type = type_to_check_first[0]  # content of Optional[...]

    type_to_checker_map = {
        list: _is_instance_of_list_type,
        dict: _is_instance_of_dict_type,
        Mapping: _is_instance_of_dict_type,
    }
    if get_origin(required_type) in type_to_checker_map:
        return type_to_checker_map[get_origin(required_type)](_object, required_type)
    return None


def _is_instance_of_list_type(_object: Any, required_list_type: Type) -> bool:
    list_item_type = get_args(required_list_type)[0]
    if is_optional_type(list_item_type) or is_union_type(list_item_type):
        list_item_type = get_args(list_item_type)
    return not (
        not isinstance(_object, list)
        or any(not isinstance(n, list_item_type) for n in _object)
    )


def _is_instance_of_dict_type(_object: Any, required_dict_type: Type) -> bool:
    key_type, value_type = get_args(required_dict_type)
    if is_optional_type(key_type) or is_union_type(key_type):
        key_type = get_args(key_type)
    if is_optional_type(value_type) or is_union_type(value_type):
        value_type = get_args(value_type)

    return not (
        not isinstance(_object, dict)
        or any(not isinstance(k, key_type) for k in _object.keys())
        or any(not isinstance(v, value_type) for v in _object.values())
    )
