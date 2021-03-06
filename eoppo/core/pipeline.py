from typing import Any, List, Dict

from eoppo.core import ObjectProcessingOperatorsPipelineABC, ObjectProcessingOperatorABC, OperatorCallParams
from eoppo.core.base import BaseObjectProcessingOperator
from eoppo.core.mixin import ObjectProcessingOperatorMixin
from eoppo.exceptions import ObjectOperatorError, ObjectProcessingError, NoOperatorsInPipelineError
from eoppo.logger import logger


__all__ = ('ObjectProcessingOperatorsPipeline',)


class ObjectProcessingOperatorsPipeline(ObjectProcessingOperatorsPipelineABC, ObjectProcessingOperatorMixin):

    def __init__(self, modules: List[BaseObjectProcessingOperator] = None,
                 ignore_processing_errors: bool = False) -> None:
        super(ObjectProcessingOperatorsPipeline, self).__init__()
        self.ignore_processing_errors = ignore_processing_errors
        self._operators = []  # type: List[BaseObjectProcessingOperator]
        if modules:
            self.extend(modules)

    def run(self, ob: Any, call_params: Dict[int, OperatorCallParams] = None) -> Any:
        if not self._operators:
            raise NoOperatorsInPipelineError()

        try:
            for idx, m in enumerate(self):
                if call_params and idx in call_params:
                    m_call_params = call_params[idx]
                    try:
                        ob = m.process(ob, callback=m_call_params.get('callback'),
                                       **m_call_params.get('params', {}))
                    except ObjectOperatorError as e:
                        skip_err = bool(m_call_params.get('skip_error'))
                        exc_to_ignore = m_call_params.get('exc_to_ignore') or tuple()
                        if not (skip_err or isinstance(e.cause, exc_to_ignore)):
                            raise
                else:
                    ob = m.process(ob)
            return ob
        except ObjectOperatorError:
            if self.ignore_processing_errors:
                return ob
            else:
                raise
        except Exception as e:
            logger.debug(f'Pipeline processing exception > {e!r}', exc_info=True)
            if self.ignore_processing_errors:
                return ob
            else:
                raise ObjectProcessingError(cause=e)

    @property
    def is_initialized(self) -> bool:
        if not self._operators:
            raise NoOperatorsInPipelineError()

        return all([m.is_initialized for m in self._operators])

    @property
    def dependencies_satisfied(self) -> bool:
        if not self._operators:
            raise NoOperatorsInPipelineError()

        return all([m.dependencies_satisfied for m in self._operators])

    @staticmethod
    def _check_item_type(v):
        if not isinstance(v, ObjectProcessingOperatorABC):
            raise TypeError(f'{v!r} is not a subclass of {ObjectProcessingOperatorABC!r}')

    def __len__(self): return len(self._operators)

    def __getitem__(self, i): return self._operators[i]

    def __delitem__(self, i): del self._operators[i]

    def __setitem__(self, i, v):
        self._check_item_type(v)
        self._operators[i] = v

    def insert(self, i, v):
        self._check_item_type(v)
        self._operators.insert(i, v)

    def __str__(self):
        return str(self._operators)
