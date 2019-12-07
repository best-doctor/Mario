from copy import deepcopy
from typing import List, Callable, Dict, Any

ContextType = Dict[str, Any]


class BasePipeline:
    __context__: ContextType = {}
    pipeline: List[Callable] = []

    def get_pipe_args(self, *args, **kwargs) -> None:
        """Fetchs arguments to calling pipe method."""
        raise NotImplementedError

    def handle_pipeline(self):
        for pipe_name in self.pipeline:
            pipe = getattr(self, pipe_name)
            pipe_args = self.get_pipe_args(pipe)

            result: Dict[str, Any] = pipe(**pipe_args)

            self.__context__.update(result)

        return result

    def run(self, **kwargs) -> ContextType:
        self.__context__ = deepcopy(kwargs)

        result = self.handle_pipeline()

        return list(result.value())[0]
