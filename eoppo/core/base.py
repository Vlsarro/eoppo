import pkg_resources
from copy import deepcopy
from typing import Callable, Any
from eoppo.logger import logger
from eoppo.core import ObjectProcessingOperatorABC
from eoppo.core.mixin import ObjectProcessingOperatorMixin
from eoppo.exceptions import (InitializationError, ObjectProcessingError, OperatorNotInitializedError,
                              DependenciesNotSatisfiedError)
from eoppo.utils.common import get_exc_data


__all__ = ('BaseObjectProcessingOperator', 'NoopObjectProcessingOperator')


class BaseObjectProcessingOperator(ObjectProcessingOperatorABC, ObjectProcessingOperatorMixin):
    _pkgs = {}  # TODO: make immutable after first assignment

    _default_settings = {}
    _dependencies = tuple()

    _dependencies_satisfied = None

    _use_globals = False

    _initialized = False
    
    def __init__(self, auto_init: bool = True, ignore_processing_errors: bool = False, **kwargs) -> None:
        super(BaseObjectProcessingOperator, self).__init__()
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
                    raise InitializationError(cause=e)
            else:
                raise DependenciesNotSatisfiedError()
        return self

    def process(self, ob: Any, callback: Callable[..., None] = None, **kwargs) -> Any:
        if not self.is_initialized:
            raise OperatorNotInitializedError()

        try:
            return self._process(ob, callback=callback, **kwargs)
        except Exception as e:
            logger.debug(f'Processing exception > {repr(e)}\n{get_exc_data()}')
            if self.ignore_processing_errors:
                return ob
            else:
                raise ObjectProcessingError(cause=e)

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


class NoopObjectProcessingOperator(BaseObjectProcessingOperator):
    def _process(self, ob: Any, callback: Callable[..., None] = None, **kwargs) -> Any:
        return ob
