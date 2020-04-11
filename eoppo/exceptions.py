"""
Global EOPPO exceptions
"""


__all__ = ('ObjectOperatorError', 'DependenciesNotSatisfiedError', 'InitializationError',
           'ObjectProcessingError', 'OperatorNotInitializedError', 'OperatorSaveError',
           'NoOperatorsInPipelineError')


class ObjectOperatorError(Exception):
    msg = 'Object operator error'

    def __init__(self, msg: str = None, cause: Exception = None):
        self.cause = cause
        msg = msg or self.msg
        super(ObjectOperatorError, self).__init__(msg)


class DependenciesNotSatisfiedError(ObjectOperatorError):
    msg = 'Object operator dependencies are not satisfied'


class InitializationError(ObjectOperatorError):
    msg = 'Object operator initialization has failed'


class OperatorNotInitializedError(ObjectOperatorError):
    msg = 'Object operator is not initialized'


class ObjectProcessingError(ObjectOperatorError):
    msg = 'Object processing has failed'


class OperatorSaveError(ObjectOperatorError):
    msg = 'Object operator saving has failed'


class NoOperatorsInPipelineError(ObjectOperatorError):
    msg = 'Pipeline does not have any operators to run'
