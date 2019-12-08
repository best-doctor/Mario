import logging
from copy import deepcopy
from typing import List, Dict, Any, Mapping

from super_mario.exceptions import ProgrammingException

ContextType = Dict[str, Any]
ImmutableContext = Mapping[str, Any]

logger = logging.getLogger(__name__)


class BasePipeline:
    __context__: ContextType = {}
    pipeline: List[str] = []

    def __init__(self):
        super().__init__()
        self.validate_pipeline_raise_on_error()

    @classmethod
    def validate_pipeline_raise_on_error(cls):
        for pipe_name in cls.pipeline:
            if pipe_name not in cls.__dict__:
                raise ProgrammingException(
                    f'{pipe_name} is not implemented in {cls.__name__}',
                )

    def get_pipe_args(self, pipe_callable) -> ImmutableContext:
        pipe_args_names = pipe_callable.__code__.co_varnames
        return {a: self.__context__[a] for a in pipe_args_names}

    def handle_pipeline(self) -> Any:
        for pipe_name in self.pipeline:
            pipe = getattr(self, pipe_name)
            pipe_args = self.get_pipe_args(pipe)
            logger.debug(f'Executing {pipe_name} with {pipe_args}...')
            result = pipe(**pipe_args)
            logger.debug(f'\t{pipe_name} finished')
            self.__context__.update(result)
        return result

    def run(self, **kwargs) -> ContextType:
        self.__context__ = deepcopy(kwargs)
        result = self.handle_pipeline()
        return list(result.values())[0]
