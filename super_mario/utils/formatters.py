from typing import Any


def strip_first(some_str: str, chars_to_strip: str) -> str:
    if some_str[0] in chars_to_strip:
        some_str = some_str[1:]
    if some_str[-1] in chars_to_strip:
        some_str = some_str[:-1]
    return some_str


def format_object_for_logging(some_data: Any, max_length: int = 100) -> str:
    raw_str_value = str(some_data)
    postfix = '' if len(raw_str_value) < max_length else '...'
    if isinstance(some_data, list):
        return f'[{strip_first(raw_str_value, "[]")[:max_length]}{postfix}]'
    elif isinstance(some_data, dict):
        return f'{{{strip_first(raw_str_value, "{}")[:max_length]}{postfix}}}'  # noqa: P103
    else:
        return f'{raw_str_value}{postfix}'
