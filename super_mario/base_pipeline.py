from __future__ import annotations

import logging
from copy import deepcopy
from typing import List, Dict, Any, Mapping, Callable, Tuple, TYPE_CHECKING
from inspect import signature

from super_mario.exceptions import ProgrammingException, GlobalContextUpdateException
from super_mario.utils.types import is_contains_only_basic_types
from super_mario.utils.formatters import format_object_for_logging

if TYPE_CHECKING:
    from typing import Type

ContextType = Dict[str, Any]
ImmutableContext = Mapping[str, Any]

logger = logging.getLogger(__name__)


class BasePipeline:
    __context__: ContextType = {}
    pipeline: List[str] = []
    initial_arguments: List[Tuple[str, Type]] = []

    def __init__(self) -> None:
        super().__init__()
        self.validate_pipeline_raise_on_error()

    @staticmethod
    def _validate_pipe_result_raise_on_error(pipe_result: ContextType, pipe_name: str) -> None:
        if not is_contains_only_basic_types(pipe_result):
            raise ProgrammingException(
                f'Pipe {pipe_name} returned non-basic types ({pipe_result})',
            )

    @classmethod
    def validate_pipeline_raise_on_error(cls) -> None:
        for pipe_name in cls.pipeline:
            if pipe_name not in cls.__dict__:
                raise ProgrammingException(
                    f'{pipe_name} is not implemented in {cls.__name__}',
                )

    @classmethod
    def validate_run_arguments_raise_on_error(
        cls,
        actual_run_arguments: Mapping[str, Any],
    ) -> None:
        if not cls.initial_arguments:
            return None
        arguments_mapping = dict(cls.initial_arguments)
        for argument_name, argument_value in actual_run_arguments.items():
            if argument_name not in arguments_mapping:
                raise ProgrammingException(
                    f'{cls.__name__}.run was called with unknown argument {argument_name}. '
                    f'All run arguments should be specified in {cls.__name__}.initial_arguments',
                )
            argument_type = arguments_mapping[argument_name]
            if argument_type is not None and not isinstance(argument_value, argument_type):
                raise ProgrammingException(
                    f'{cls.__name__}.run was called with argument {argument_name} of type '
                    f'{type(argument_value).__name__}, but it is specified '
                    f'to be of type {argument_type}.',
                )

    def get_pipe_signature_args(self, pipe_callable: Callable) -> Tuple[str, ...]:
        pipe_func = getattr(pipe_callable, '__func__', pipe_callable)
        pipe_signature = signature(pipe_func)
        pipe_args_names = pipe_signature.parameters.keys()
        return tuple(pipe_args_names)

    def get_pipe_args(self, pipe_callable: Callable) -> ImmutableContext:
        pipe_args_names = self.get_pipe_signature_args(pipe_callable)
        for arg_name in pipe_args_names:
            if arg_name not in self.__context__:
                raise ProgrammingException(
                    f'Argument "{arg_name}" not found when executing '
                    f'{type(self).__name__}.{pipe_callable.__name__}',
                )
        return {a: self.__context__[a] for a in pipe_args_names}

    def handle_pipeline(self) -> ContextType:
        for pipe_name in self.pipeline:
            pipe = getattr(self, pipe_name)
            pipe_args = self.get_pipe_args(pipe)

            logger.debug(
                f'Executing {pipe_name} with {format_object_for_logging(pipe_args)}...',
            )
            result = pipe(**pipe_args)
            logger.debug(f'\t{pipe_name} finished')

            if result:
                self._validate_pipe(result, pipe_name)
                self.__context__.update(result)
        return result

    def run(self, **kwargs: Any) -> ContextType:
        self.validate_run_arguments_raise_on_error(kwargs)
        self.__context__ = deepcopy(kwargs)
        result = self.handle_pipeline()
        return list(result.values())[0] if result else None

    def _validate_implicit_context_update(self, result: ContextType, pipe_name: str) -> None:
        for result_key in result.keys():
            if result_key in self.__context__.keys():
                raise GlobalContextUpdateException(
                    f'Pipe {pipe_name} tried to update context with existed keys.',
                )

    def _validate_pipe(self, result: ContextType, pipe_name: str) -> None:
        pipe_validators = (
            self._validate_pipe_result_raise_on_error,
            self._validate_implicit_context_update,
        )

        for pipe_validator in pipe_validators:
            pipe_validator(result, pipe_name)
