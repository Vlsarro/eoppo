import pkg_resources
from copy import deepcopy
from eippm.core import ImageProcessingModuleABC
from eippm.core.mixin import ImageProcessingModuleMixin


class BaseImageProcessingModule(ImageProcessingModuleABC, ImageProcessingModuleMixin):
    _pkgs = {}

    _default_settings = {}
    _dependencies = tuple()

    _dependencies_satisfied = None
    
    def __init__(self):
        super(BaseImageProcessingModule, self).__init__()
        self.settings = deepcopy(self._default_settings)

    def initialize(self):
        self._initialized = True

    @property
    def dependencies_satisfied(self):
        if self._dependencies_satisfied is None:
            self._dependencies_satisfied = True
            if self._dependencies:
                try:
                    pkg_resources.require(self._dependencies)
                except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
                    self._dependencies_satisfied = False
                finally:
                    return self._dependencies_satisfied
        return self._dependencies_satisfied
