import pytest

from super_mario.base_pipeline import BasePipeline
from super_mario.decorators import process_pipe


@pytest.fixture
def simple_pipeline():
    class SimplePipeline(BasePipeline):
        pipeline = [
            'simple_pipe',
        ]

        @process_pipe
        def simple_pipe(simple_arg):
            another_simple_arg = 100500
            return {'result': [simple_arg, another_simple_arg]}

    return SimplePipeline()


def test_get_pipe_args(simple_pipeline):
    pipe_args = simple_pipeline.get_pipe_signature_args(simple_pipeline.simple_pipe)

    assert 'simple_arg' in pipe_args
    assert 'another_simple_arg' not in pipe_args
