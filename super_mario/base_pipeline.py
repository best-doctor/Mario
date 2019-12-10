import logging
from copy import deepcopy
from typing import List, Dict, Any, Mapping

from super_mario.exceptions import ProgrammingException, GlobalContextUpdateException
from super_mario.utils.types import is_contains_only_basic_types

ContextType = Dict[str, Any]
ImmutableContext = Mapping[str, Any]

logger = logging.getLogger(__name__)


class BasePipeline:
    __context__: ContextType = {}
    pipeline: List[str] = []

    def __init__(self) -> None:
        super().__init__()
        self.validate_pipeline_raise_on_error()

    @classmethod
    def validate_pipeline_raise_on_error(cls) -> None:
        for pipe_name in cls.pipeline:
            if pipe_name not in cls.__dict__:
                raise ProgrammingException(
                    f'{pipe_name} is not implemented in {cls.__name__}',
                )

    def get_pipe_args(self, pipe_callable) -> ImmutableContext:
        pipe_args_names = pipe_callable.__code__.co_varnames
        return {a: self.__context__[a] for a in pipe_args_names}

    def handle_pipeline(self) -> ContextType:
        for pipe_name in self.pipeline:
            pipe = getattr(self, pipe_name)
            pipe_args = self.get_pipe_args(pipe)

            logger.debug(f'Executing {pipe_name} with {pipe_args}...')
            result = pipe(**pipe_args)

            self._validate_pipe(result, pipe_name)

            logger.debug(f'\t{pipe_name} finished')
            self.__context__.update(result)
        return result

    def run(self, **kwargs) -> ContextType:
        self.__context__ = deepcopy(kwargs)
        result = self.handle_pipeline()
        return list(result.values())[0]

    def _validate_pipe(self, result: ContextType, pipe_name: str) -> None:
        pipe_validators = (
            self._validate_pipe_result_raise_on_error,
            self._validate_implicit_context_update,
        )

        for pipe_validator in pipe_validators:
            pipe_validator(result, pipe_name)

    @staticmethod
    def _validate_pipe_result_raise_on_error(pipe_result: ContextType, pipe_name: str) -> None:
        if not is_contains_only_basic_types(pipe_result):
            raise ProgrammingException(
                f'Pipe {pipe_name} returned non-basic types ({pipe_result})',
            )

    def _validate_implicit_context_update(self, result: ContextType, pipe_name: str) -> None:
        for result_key in result.keys():
            if result_key in self.__context__.keys():
                raise GlobalContextUpdateException(
                    f'Pipe {pipe_name} tried to update context with existed keys.',
                )
