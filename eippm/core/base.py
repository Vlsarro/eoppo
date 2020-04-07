import pkg_resources
from copy import deepcopy
from typing import Callable, Any
from eippm.logger import logger
from eippm.core import ImageProcessingModuleABC
from eippm.core.mixin import ImageProcessingModuleMixin
from eippm.exceptions import (EIPPMInitializationException, EIPPMUnhandledException, EIPPMNotInitializedException,
                              EIPPMDependenciesNotSatisfiedException)
from eippm.utils.common import get_exc_data


__all__ = ('BaseImageProcessingModule',)


class BaseImageProcessingModule(ImageProcessingModuleABC, ImageProcessingModuleMixin):
    _pkgs = {}  # TODO: make immutable after first assignment

    _default_settings = {}
    _dependencies = tuple()

    _dependencies_satisfied = None

    _use_globals = False

    _initialized = False
    
    def __init__(self, auto_init: bool = True, ignore_processing_errors: bool = False, **kwargs) -> None:
        super(BaseImageProcessingModule, self).__init__()
        self.settings = deepcopy(self._default_settings)
        self.ignore_processing_errors = ignore_processing_errors
        if auto_init:
            self.initialize(**kwargs)

    def _initialize(self, **kwargs) -> __qualname__:
        if self._use_globals:
            self._pkgs = globals()
        self._initialized = True
        return self

    def initialize(self, **kwargs) -> __qualname__:
        if not self.is_initialized:
            if self.dependencies_satisfied:
                try:
                    return self._initialize(**kwargs)
                except Exception as e:
                    logger.debug(f'Initialization exception > {repr(e)}\n{get_exc_data()}')
                    raise EIPPMInitializationException(cause=e)
            else:
                raise EIPPMDependenciesNotSatisfiedException()
        return self

    def _process(self, image: Any, callback: Callable = None, **kwargs) -> Any:
        return image

    def process(self, image: Any, callback: Callable = None, **kwargs) -> Any:
        if not self.is_initialized:
            raise EIPPMNotInitializedException()

        try:
            return self._process(image, callback=callback, **kwargs)
        except Exception as e:
            logger.debug(f'Processing exception > {repr(e)}\n{get_exc_data()}')
            if self.ignore_processing_errors:
                return image
            else:
                raise EIPPMUnhandledException(cause=e)

    @property
    def dependencies_satisfied(self) -> bool:
        if self._dependencies_satisfied is None:
            self._dependencies_satisfied = True
            if self._dependencies:
                try:
                    pkg_resources.require(self._dependencies)
                except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict) as e:
                    logger.debug(f'Dependencies are not satisfied > {repr(e)}\n{get_exc_data()}')
                    self._dependencies_satisfied = False
                finally:
                    return self._dependencies_satisfied
        return self._dependencies_satisfied

    @property
    def is_initialized(self) -> bool:
        return self._initialized
