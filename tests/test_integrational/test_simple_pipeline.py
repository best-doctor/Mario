from super_mario import BasePipeline, process_pipe


def test_simple_pipeline():
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

    assert result == 20


def test_no_static_method_pipeline():
    class SimplePipeline(BasePipeline):
        pipeline = [
            'sum_numbers',
            'sum_numbers_again',
            'multiply_numbers',
        ]

        @staticmethod
        @process_pipe
        def sum_numbers(a, b):
            return {'d': a + b}

        @process_pipe
        @staticmethod
        def sum_numbers_again(d):
            return {'e': d + 2}

        @process_pipe
        def multiply_numbers(e, d):
            return {'f': e * d}

    result = SimplePipeline().run(a=2, b=3, c=4)

    assert result == 35


def test_works_when_nonlast_pipe_returns_nothing():
    class SimplePipeline(BasePipeline):
        pipeline = [
            'sum_numbers',
            'sum_numbers_again',
        ]

        @staticmethod
        @process_pipe
        def sum_numbers(a):
            return None

        @process_pipe
        @staticmethod
        def sum_numbers_again(a):
            return {'b': a + 2}

    result = SimplePipeline().run(a=2)

    assert result == 4
