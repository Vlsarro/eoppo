from abc import ABC, abstractmethod


__all__ = ('ImageProcessingModuleABC', 'ImageProcessingModulesPipelineABC', 'ImageProcessingModuleMixin')


class ImageProcessingModuleABC(ABC):

    @abstractmethod
    def process(self, image, callback=None):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def initialize(self):
        pass


class ImageProcessingModulesPipelineABC(ABC):

    @abstractmethod
    def run(self):
        pass


class ImageProcessingModuleMixin:
    _initialized = False

    @property
    def is_initialized(self):
        return self._initialized
