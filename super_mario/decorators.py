import inspect
from typing import Callable, Any, Tuple, Dict

import wrapt


def _static_method_by_default(
    wrapped: Callable,
    instance: Any,
    args: Tuple[Any],
    kwargs: Dict[str, Any],
) -> Callable:
    """
    Make decorator behaves like @staticmethod.

    If decorator applied to static method, id does nothing.
    If decorator applied to non-static method, it makes it static.
    """
    if instance is not None and not inspect.isclass(instance):
        return instance.__class__.__dict__[wrapped.__name__](*args, **kwargs)
    return wrapped(*args, **kwargs)


@wrapt.decorator
def base_pipe_decorator(
    wrapped: Callable,
    instance: Any,
    args: Tuple[Any],
    kwargs: Dict[str, Any],
) -> Callable:
    return _static_method_by_default(wrapped, instance, args, kwargs)


input_pipe = base_pipe_decorator
process_pipe = base_pipe_decorator
output_pipe = base_pipe_decorator
