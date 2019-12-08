import pytest

from super_mario import BasePipeline, process_pipe
from super_mario.exceptions import ProgrammingException


def test_lack_of_pipes_raises_error():
    class SimplePipeline(BasePipeline):
        pipeline = [
            'sum_numbers',
            'multiply_numbers',
        ]

        @process_pipe
        def sum_numbers(a, b):
            return {'c': a + b}

    with pytest.raises(ProgrammingException):
        SimplePipeline()
