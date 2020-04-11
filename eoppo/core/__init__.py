from abc import ABC, abstractmethod
from collections import MutableSequence


__all__ = ('ObjectProcessingOperatorABC', 'ObjectProcessingOperatorsPipelineABC')


class ObjectProcessingOperatorABC(ABC):

    @abstractmethod
    def _process(self, ob, callback=None, **kwargs):
        pass

    @abstractmethod
    def process(self, ob, callback=None, **kwargs):
        pass

    @abstractmethod
    def _initialize(self, **kwargs):
        pass

    @abstractmethod
    def initialize(self, **kwargs):
        pass


class ObjectProcessingOperatorsPipelineABC(MutableSequence):

    @abstractmethod
    def run(self, ob, call_params=None):
        pass
