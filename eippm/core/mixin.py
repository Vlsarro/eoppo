from eippm.exceptions import EIPPMSaveException
from eippm.logger import logger
from eippm.utils.version import get_version
from eippm.utils.common import get_exc_data

try:
    import cPickle as pickle
except:
    import pickle


__all__ = ('ImageProcessingModuleMixin',)


class ImageProcessingModuleMixin:
    _initialized = False
    _version = tuple()

    @property
    def is_initialized(self):
        return self._initialized

    @property
    def version(self):
        return get_version(self._version)

    @property
    def name(self):
        return f'{self.__class__.__name__}_v{self.version}'

    def save(self, filename: str) -> None:
        try:
            with open(filename, 'wb') as f:
                pickle.dump(self, f)
        except Exception as e:
            logger.debug(f'Module saving exception > {repr(e)}\n{get_exc_data()}')
            raise EIPPMSaveException(cause=e)
