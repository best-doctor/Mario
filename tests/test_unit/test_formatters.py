from super_mario.utils.formatters import format_object_for_logging


def test_format_object_for_logging():
    assert format_object_for_logging(list(range(100)), max_length=10) == '[0, 1, 2, 3...]'
