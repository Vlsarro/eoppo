import sys
import traceback


__all__ = ('get_exc_data',)


def get_exc_data():
    exc_type, exc, tb = sys.exc_info()
    return ''.join(traceback.format_exception(exc_type, exc, tb))
