from copy import deepcopy
from typing import List, Dict, Any, Mapping

ContextType = Dict[str, Any]
ImmutableContext = Mapping[str, Any]


class BasePipeline:
    __context__: ContextType = {}
    pipeline: List[str] = []

    def get_pipe_args(self, pipe_callable) -> ImmutableContext:
        pipe_args_names = pipe_callable.__code__.co_varnames
        return {a: self.__context__[a] for a in pipe_args_names}

    def handle_pipeline(self) -> Any:
        for pipe_name in self.pipeline:
            pipe = getattr(self, pipe_name)
            pipe_args = self.get_pipe_args(pipe)
            result = pipe(**pipe_args)
            self.__context__.update(result)
        return result

    def run(self, **kwargs) -> ContextType:
        self.__context__ = deepcopy(kwargs)
        result = self.handle_pipeline()
        return list(result.values())[0]
