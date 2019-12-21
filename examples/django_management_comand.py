from super_mario import process_pipe
from super_mario.binders.django import PipelineForDjangoManagementCommand


class Command(PipelineForDjangoManagementCommand):
    pipeline = [
        'sum_numbers',
        'multiply_numbers',
    ]

    def add_arguments(self, parser) -> None:
        parser.add_argument('-a', type=int)

    def get_pipeline_kwargs(self, command_options):
        return {'a': command_options['a'], 'b': 2, 'c': 3}

    @process_pipe
    @staticmethod
    def sum_numbers(a, b):
        return {'d': a + b}

    @process_pipe
    @staticmethod
    def multiply_numbers(c, d):
        return {'e': c * d}
