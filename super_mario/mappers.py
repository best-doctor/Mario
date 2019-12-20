from typing import Any, Type, NamedTuple


def map_object_to_namedtuple(obj: Any, namedtuple_type: Type[NamedTuple]) -> NamedTuple:
    namedtuple_kwargs = {}
    for field_name, _ in namedtuple_type._field_types.items():
        field_value = getattr(obj, field_name)
        namedtuple_kwargs[field_name] = field_value
    return namedtuple_type(**namedtuple_kwargs)
