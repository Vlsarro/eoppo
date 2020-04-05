import pkg_resources
from copy import deepcopy
from eippm.logger import logger
from eippm.core import ImageProcessingModuleABC
from eippm.core.exceptions import (EIPPMInitializationException, EIPPMUnhandledException, EIPPMNotInitializedException,
                                   EIPPMDependenciesNotSatisfiedException)
from eippm.core.mixin import ImageProcessingModuleMixin
from eippm.utils.common import get_exc_data


class BaseImageProcessingModule(ImageProcessingModuleABC, ImageProcessingModuleMixin):
    _pkgs = {}

    _default_settings = {}
    _dependencies = tuple()

    _dependencies_satisfied = None
    
    def __init__(self) -> None:
        super(BaseImageProcessingModule, self).__init__()
        self.settings = deepcopy(self._default_settings)

    def _initialize(self, **kwargs) -> None:
        self._initialized = True

    def initialize(self, **kwargs) -> None:
        if not self.is_initialized:
            if self.dependencies_satisfied:
                try:
                    self._initialize(**kwargs)
                except Exception as e:
                    logger.debug(f'Initialization exception > {repr(e)}\n{get_exc_data()}')
                    raise EIPPMInitializationException(cause=e)
            else:
                raise EIPPMDependenciesNotSatisfiedException()

    def _process(self, image, callback=None, **kwargs):
        return image

    def process(self, image, callback=None, **kwargs):
        if not self.is_initialized:
            raise EIPPMNotInitializedException()

        try:
            return self._process(image, callback=callback, **kwargs)
        except Exception as e:
            logger.debug(f'Processing exception > {repr(e)}\n{get_exc_data()}')
            raise EIPPMUnhandledException(cause=e)

    @property
    def dependencies_satisfied(self) -> bool:
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
