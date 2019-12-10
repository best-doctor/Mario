import pytest

from super_mario.base_pipeline import BasePipeline
from super_mario.decorators import process_pipe
from super_mario.exceptions import GlobalContextUpdateException


@pytest.fixture
def simple_pipeline():
    class SimplePipeline(BasePipeline):
        pipeline = [
            'sum_numbers',
            'multiply_numbers',
        ]

        @process_pipe
        def sum_numbers(a, b):
            return {'d': a + b}

        @process_pipe
        def multiply_numbers(c, d):
            return {'d': c * d}

    return SimplePipeline()


def test_context_update_raises_exception(simple_pipeline):
    with pytest.raises(GlobalContextUpdateException):
        simple_pipeline.run(a=1, b=2, c=3)
