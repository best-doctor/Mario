from __future__ import annotations

from typing import Any, NamedTuple, TYPE_CHECKING

from super_mario.exceptions import ProgrammingException
from super_mario.utils.types import is_instance_of_type

if TYPE_CHECKING:
    from typing import Type


def map_object_to_namedtuple(
    obj: Any,
    namedtuple_type: Type[NamedTuple],
    check_types: bool = True,
) -> NamedTuple:
    namedtuple_kwargs = {}
    for field_name, field_type in namedtuple_type.__annotations__.items():
        field_value = getattr(obj, field_name)
        if check_types and is_instance_of_type(field_value, field_type) is False:
            raise ProgrammingException(
                f'{obj}.{field_name} does not match type of '
                f'{namedtuple_type.__name__}.{field_name} ({field_type})',
            )
        namedtuple_kwargs[field_name] = field_value
    return namedtuple_type(**namedtuple_kwargs)
