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
    _version = tuple()

    @property
    def version(self) -> str:
        return get_version(self._version)

    @property
    def short_name(self) -> str:
        return self.__class__.__name__

    @property
    def full_name(self) -> str:
        return f'{self.short_name} ({self.version})'

    def save(self, filepath: str) -> __qualname__:
        try:
            with open(filepath, 'wb') as f:
                pickle.dump(self, f)
        except Exception as e:
            logger.debug(f'Module saving exception > {repr(e)}\n{get_exc_data()}')
            raise EIPPMSaveException(cause=e)
        else:
            return self

    def __repr__(self) -> str:
        return f'{self.short_name}({hex(id(self))})'
