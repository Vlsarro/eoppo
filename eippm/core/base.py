from copy import deepcopy
from eippm.core import ImageProcessingModuleABC
from eippm.core.mixin import ImageProcessingModuleMixin


class BaseImageProcessingModule(ImageProcessingModuleABC, ImageProcessingModuleMixin):
    
    default_settings = {}
    
    def __init__(self):
        super(BaseImageProcessingModule, self).__init__()
        self.settings = deepcopy(self.default_settings)

    def initialize(self):
        self._initialized = True
