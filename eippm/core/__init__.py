from abc import ABC, abstractmethod
from collections import MutableSequence


__all__ = ('ImageProcessingModuleABC', 'ImageProcessingModulesPipelineABC')


class ImageProcessingModuleABC(ABC):

    @abstractmethod
    def _process(self, image, callback=None, **kwargs):
        pass

    @abstractmethod
    def process(self, image, callback=None, **kwargs):
        pass

    @abstractmethod
    def _initialize(self, **kwargs):
        pass

    @abstractmethod
    def initialize(self, **kwargs):
        pass


class ImageProcessingModulesPipelineABC(MutableSequence):

    @abstractmethod
    def run(self, image, call_params=None):
        pass
