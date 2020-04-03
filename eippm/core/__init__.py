from abc import ABC, abstractmethod


__all__ = ('ImageProcessingModuleABC',)


class ImageProcessingModuleABC(ABC):

    @abstractmethod
    def process(self, image):
        pass

    @abstractmethod
    def save(self):
        pass
