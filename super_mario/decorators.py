import inspect

import wrapt


def _static_method_by_default(wrapped, instance, args, kwargs):
    """
    Make decorator behaves like @staticmethod.

    If decorator applied to static method, id does nothing.
    If decorator applied to non-static method, it makes it static.
    """
    if instance is not None and not inspect.isclass(instance):
        return instance.__class__.__dict__[wrapped.__name__](*args, **kwargs)
    return wrapped(*args, **kwargs)


@wrapt.decorator
def input_pipe(wrapped, instance, args, kwargs):
    return _static_method_by_default(wrapped, instance, args, kwargs)


@wrapt.decorator
def process_pipe(wrapped, instance, args, kwargs):
    return _static_method_by_default(wrapped, instance, args, kwargs)


@wrapt.decorator
def output_pipe(wrapped, instance, args, kwargs):
    return _static_method_by_default(wrapped, instance, args, kwargs)
