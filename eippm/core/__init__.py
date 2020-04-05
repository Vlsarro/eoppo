from abc import ABC, abstractmethod


__all__ = ('ImageProcessingModuleABC', 'ImageProcessingModulesPipelineABC')


class ImageProcessingModuleABC(ABC):

    @abstractmethod
    def _process(self, image, callback=None, **kwargs):
        pass

    @abstractmethod
    def process(self, image, callback=None, **kwargs):
        pass

    @abstractmethod
    def save(self, filename: str):
        pass

    @abstractmethod
    def _initialize(self, **kwargs):
        pass

    @abstractmethod
    def initialize(self, **kwargs):
        pass


class ImageProcessingModulesPipelineABC(ABC):

    @abstractmethod
    def run(self):
        pass
