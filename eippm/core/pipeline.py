from typing import Any, List, Dict, TypedDict, Callable, Tuple

from eippm.core import ImageProcessingModulesPipelineABC, ImageProcessingModuleABC
from eippm.core.base import BaseImageProcessingModule
from eippm.core.mixin import ImageProcessingModuleMixin
from eippm.exceptions import EIPPMException, EIPPMUnhandledException, EIPPMNoModulesInPipelineException
from eippm.logger import logger
from eippm.utils.common import get_exc_data


__all__ = ('ImageProcessingModulesPipeline',)


class ModuleCallParams(TypedDict):
    callback: Callable[..., None]
    params: Dict
    exc_to_ignore: Tuple[Exception]
    skip_error: bool


class ImageProcessingModulesPipeline(ImageProcessingModulesPipelineABC, ImageProcessingModuleMixin):

    def __init__(self, modules: List[BaseImageProcessingModule] = None, ignore_processing_errors: bool = False) -> None:
        super(ImageProcessingModulesPipeline, self).__init__()
        self.ignore_processing_errors = ignore_processing_errors
        self._modules = []  # type: List[BaseImageProcessingModule]
        if modules:
            self.extend(modules)

    def run(self, image: Any, call_params: Dict[int, ModuleCallParams] = None) -> Any:
        if not self._modules:
            raise EIPPMNoModulesInPipelineException()

        try:
            for idx, m in enumerate(self):
                if call_params and idx in call_params:
                    # TODO: add warning for idx miss, just try except with key error and warn in exc handler
                    m_call_params = call_params[idx]
                    try:
                        image = m.process(image, callback=m_call_params.get('callback'),
                                          **m_call_params.get('params', {}))
                    except m_call_params.get('exc_to_ignore'):
                        pass
                    except Exception:
                        if not bool(m_call_params.get('skip_error')):
                            raise
                else:
                    image = m.process(image)
            return image
        except EIPPMException:
            if self.ignore_processing_errors:
                return image
            else:
                raise
        except Exception as e:
            logger.debug(f'Pipeline processing exception > {repr(e)}\n{get_exc_data()}')
            if self.ignore_processing_errors:
                return image
            else:
                raise EIPPMUnhandledException(cause=e)

    @property
    def is_initialized(self) -> bool:
        if not self._modules:
            raise EIPPMNoModulesInPipelineException()

        return all([m.is_initialized for m in self._modules])

    @property
    def dependencies_satisfied(self) -> bool:
        if not self._modules:
            raise EIPPMNoModulesInPipelineException()

        return all([m.dependencies_satisfied for m in self._modules])

    @staticmethod
    def _check_item_type(v):
        if not isinstance(v, ImageProcessingModuleABC):
            raise TypeError(v)

    def __len__(self): return len(self._modules)

    def __getitem__(self, i): return self._modules[i]

    def __delitem__(self, i): del self._modules[i]

    def __setitem__(self, i, v):
        self._check_item_type(v)
        self._modules[i] = v

    def insert(self, i, v):
        self._check_item_type(v)
        self._modules.insert(i, v)

    def __str__(self):
        return str(self._modules)
