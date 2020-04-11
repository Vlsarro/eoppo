from abc import ABC, abstractmethod
from collections import MutableSequence
from typing import Any, Callable, Dict, TypedDict, Tuple, Union


__all__ = ('ObjectProcessingOperatorABC', 'ObjectProcessingOperatorsPipelineABC', 'OperatorCallParams')


class ObjectProcessingOperatorABC(ABC):

    @abstractmethod
    def _process(self, ob: Any, callback: Callable = None, **kwargs) -> Any:
        pass

    @abstractmethod
    def process(self, ob: Any, callback: Callable = None, **kwargs) -> Any:
        pass

    @abstractmethod
    def _initialize(self, **kwargs) -> None:
        pass

    @abstractmethod
    def initialize(self, **kwargs) -> None:
        pass


class OperatorCallParams(TypedDict):
    callback: Callable[..., None]
    params: Dict
    exc_to_ignore: Union[type, Tuple[Exception]]
    skip_error: bool


class ObjectProcessingOperatorsPipelineABC(MutableSequence):

    @abstractmethod
    def run(self, ob: Any, call_params: Dict[int, OperatorCallParams] = None) -> Any:
        pass
