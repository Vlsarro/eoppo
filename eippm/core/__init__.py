from abc import ABC, abstractmethod


__all__ = ('ImageProcessingModuleABC', 'ImageProcessingModulesPipelineABC')


class ImageProcessingModuleABC(ABC):

    @abstractmethod
    def process(self, image):
        pass

    @abstractmethod
    def save(self):
        pass


class ImageProcessingModulesPipelineABC(ABC):

    @abstractmethod
    def run(self):
        pass
