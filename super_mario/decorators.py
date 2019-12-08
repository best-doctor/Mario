import wrapt


@wrapt.decorator
def input_pipe(wrapped, instance, args, kwargs):
    return wrapped(*args, **kwargs)


@wrapt.decorator
def process_pipe(wrapped, instance, args, kwargs):
    return wrapped(*args, **kwargs)


@wrapt.decorator
def output_pipe(wrapped, instance, args, kwargs):
    return wrapped(*args, **kwargs)
