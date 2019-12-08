import logging

from super_mario import BasePipeline, process_pipe


logging.basicConfig(level=logging.DEBUG)


class SimplePipeline(BasePipeline):
    pipeline = [
        'sum_numbers',
        'multiply_numbers',
    ]

    @process_pipe
    @staticmethod
    def sum_numbers(a, b):
        return {'d': a + b}

    @process_pipe
    @staticmethod
    def multiply_numbers(c, d):
        return {'e': c * d}


result = SimplePipeline().run(a=2, b=3, c=4)
print(result)
