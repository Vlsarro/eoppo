from abc import ABC, abstractmethod


__all__ = ('ImageProcessingModuleABC', 'ImageProcessingModulesPipelineABC')


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
