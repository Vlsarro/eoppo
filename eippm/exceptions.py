__all__ = ('EIPPMException', 'EIPPMDependenciesNotSatisfiedException', 'EIPPMInitializationException',
           'EIPPMUnhandledException', 'EIPPMNotInitializedException', 'EIPPMSaveException',
           'EIPPMNoModulesInPipelineException')


class EIPPMException(Exception):
    msg = 'Processing exception'
    code = '1'

    def __init__(self, msg=None, cause=None):
        self.cause = cause
        msg = msg or self.msg
        super(EIPPMException, self).__init__(msg)


class EIPPMDependenciesNotSatisfiedException(EIPPMException):
    code = '2'


class EIPPMInitializationException(EIPPMException):
    code = '3'


class EIPPMNotInitializedException(EIPPMException):
    code = '4'


class EIPPMUnhandledException(EIPPMException):
    code = '5'


class EIPPMSaveException(EIPPMException):
    code = '6'


class EIPPMNoModulesInPipelineException(EIPPMException):
    code = '7'
