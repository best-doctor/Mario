from datetime import datetime, date
from decimal import Decimal
from typing import Any, NamedTuple

from super_mario.utils.lists import flat


def is_contains_only_basic_types(some_data: Any) -> bool:
    allowed_containers = [
        dict,
        list,
        tuple,
    ]
    allowed_types = [
        int,
        float,
        str,
        datetime,
        Decimal,
        date,
        NamedTuple,
    ]

    if some_data is None:
        return True

    if isinstance(some_data, tuple(allowed_containers)):
        if isinstance(some_data, dict):
            subitems = flat(some_data.items())
        else:
            subitems = some_data
        return all(is_contains_only_basic_types(d) for d in subitems)
    return isinstance(some_data, tuple(allowed_types))
