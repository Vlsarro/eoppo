import sys

from abc import ABC, abstractmethod
from collections import MutableSequence
from typing import Any, Callable, Dict, Tuple, Union

if sys.version_info[0] == 3 and sys.version_info[1] >= 8:
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = ('ObjectProcessingOperatorABC', 'ObjectProcessingOperatorsPipelineABC', 'OperatorCallParams')


class ObjectProcessingOperatorABC(ABC):

    @abstractmethod
    def _process(self, ob: Any, callback: Callable[..., None] = None, **kwargs) -> Any:
        pass

    @abstractmethod
    def process(self, ob: Any, callback: Callable[..., None] = None, **kwargs) -> Any:
        pass

    @abstractmethod
    def _initialize(self, **kwargs) -> __qualname__:
        pass

    @abstractmethod
    def initialize(self, **kwargs) -> __qualname__:
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
