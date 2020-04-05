from eippm.utils.version import get_version


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
