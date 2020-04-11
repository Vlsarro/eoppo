from eoppo.exceptions import OperatorSaveError
from eoppo.logger import logger
from eoppo.utils.version import get_version
from eoppo.utils.common import get_exc_data

try:
    import cPickle as pickle
except:
    import pickle


__all__ = ('ObjectProcessingOperatorMixin',)


class ObjectProcessingOperatorMixin:
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
            logger.debug(f'Operator saving exception > {repr(e)}\n{get_exc_data()}')
            raise OperatorSaveError(cause=e)
        else:
            return self

    def __repr__(self) -> str:
        return f'{self.short_name}({hex(id(self))})'
