from eippm.core import ImageProcessingModuleABC, ImageProcessingModuleMixin


class BaseImageProcessingModule(ImageProcessingModuleABC, ImageProcessingModuleMixin):

    def initialize(self):
        self._initialized = True
