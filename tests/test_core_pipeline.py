import pkg_resources
from unittest import mock, main
from typing import Callable

from tests import EIPPMBaseTestCase
from eoppo.core.base import BaseObjectProcessingOperator
from eoppo.core.pipeline import ObjectProcessingOperatorsPipeline
from eoppo.exceptions import ObjectProcessingError


class TestOperator1(BaseObjectProcessingOperator):
    callback_msg = 'TestModule1 called'

    def _process(self, ob: int, callback: Callable = None, **kwargs) -> int:
        if callback:
            callback(data=self.callback_msg)
        return ob + 5


class TestOperator2(BaseObjectProcessingOperator):
    callback_msg = 'TestModule2 called'

    def _process(self, ob: int, callback: Callable = None, extra_num=0, **kwargs) -> int:
        if callback:
            callback(data=self.callback_msg)
        return ob + 6 + extra_num


class TestOperator3(BaseObjectProcessingOperator):
    callback_msg = 'TestModule3 called'

    def _process(self, ob: int, callback: Callable = None, extra_num=0, **kwargs) -> int:
        if callback:
            callback(data=self.callback_msg)
        return ob + 7 + extra_num


class TestModule4(TestOperator3):

    def process(self, ob: int, callback: Callable[..., None] = None, **kwargs) -> int:
        raise ValueError('test error')


class TestObjectProcessingOperatorsPipeline(ObjectProcessingOperatorsPipeline):
    _version = (0, 0, 1, 'alpha', 0)


class ImageProcessingModulesPipelineTests(EIPPMBaseTestCase):

    def create_default_test_obj(self):
        return TestObjectProcessingOperatorsPipeline([])

    def test_run_simple(self):
        pipeline = TestObjectProcessingOperatorsPipeline([TestOperator1(), TestOperator2(), TestOperator3()])
        result = pipeline.run(0)
        self.assertEqual(18, result)

    def test_run_unhandled_error(self):
        pipeline = TestObjectProcessingOperatorsPipeline([TestOperator1(), TestModule4()])
        with self.assertRaises(ObjectProcessingError) as cm:
            pipeline.run(0)
        self.assertIsInstance(cm.exception.cause, ValueError)

    def test_run_processing_error(self):
        pipeline = TestObjectProcessingOperatorsPipeline([TestOperator1(), TestOperator3()])
        with self.assertRaises(ObjectProcessingError) as cm:
            pipeline.run(0, call_params={
                1: {
                    'params': {
                        'extra_num': 'not_an_integer'
                    }
                }
            })
        self.assertIsInstance(cm.exception.cause, TypeError)

    def test_run_unhandled_error_ignore(self):
        pipeline = TestObjectProcessingOperatorsPipeline([TestOperator1(), TestModule4()],
                                                         ignore_processing_errors=True)
        result = pipeline.run(0)
        self.assertEqual(5, result)

    def test_run_processing_error_ignore(self):
        pipeline = TestObjectProcessingOperatorsPipeline([TestOperator1(), TestOperator3()],
                                                         ignore_processing_errors=True)
        result = pipeline.run(0, call_params={
            1: {
                'params': {
                    'extra_num': 'not_an_integer'
                }
            }
        })
        self.assertEqual(5, result)

    def test_run_call_params(self):
        m1 = TestOperator1()
        m2 = TestOperator2()
        m3 = TestOperator3()

        pipeline = TestObjectProcessingOperatorsPipeline([m1, m2, m3])

        call_params = {
            0: {'callback': lambda data: self.assertEqual(m1.callback_msg, data)},
            1: {
                'callback': lambda data: self.assertEqual(m2.callback_msg, data),
                'params': {
                    'extra_num': 5
                }
            },
            2: {
                'callback': lambda data: self.assertEqual(m3.callback_msg, data),
                'params': {
                    'extra_num': 'not_a_num'
                },
                'skip_error': True
            }
        }

        result = pipeline.run(0, call_params=call_params)
        self.assertEqual(16, result)

        call_params[2]['skip_error'] = False
        with self.assertRaises(ObjectProcessingError) as cm:
            pipeline.run(0, call_params=call_params)

        self.assertIsInstance(cm.exception.cause, TypeError)

        call_params[2]['exc_to_ignore'] = (TypeError,)

        result = pipeline.run(0, call_params=call_params)
        self.assertEqual(16, result)

    def test_run_call_params_invalid_idx(self):
        pipeline = TestObjectProcessingOperatorsPipeline([TestOperator1(), TestOperator3()])
        result = pipeline.run(0, call_params={325435: {}})
        self.assertEqual(12, result)

    def test_pipeline_props(self):
        m1 = TestOperator1(auto_init=False)
        m2 = TestOperator2(auto_init=False)
        m3 = TestOperator3()

        pipeline = TestObjectProcessingOperatorsPipeline([m1, m2, m3])
        self.assertFalse(pipeline.is_initialized)

        m1.initialize()
        m2.initialize()
        self.assertTrue(pipeline.is_initialized)

        self.assertEqual('0.0.1', pipeline.version)

        self.assertEqual('TestObjectProcessingOperatorsPipeline (0.0.1)', pipeline.full_name)
        self.assertEqual('TestObjectProcessingOperatorsPipeline', pipeline.short_name)

        with mock.patch('pkg_resources.require') as mock_require:
            res = pipeline.dependencies_satisfied
            self.assertTrue(res)

            m4 = TestOperator3(auto_init=False)
            m4._dependencies = self.test_dependencies

            pipeline.append(m4)

            mock_require.side_effect = [pkg_resources.VersionConflict(), None]

            res = pipeline.dependencies_satisfied
            self.assertFalse(res)

            m4._dependencies_satisfied = None
            res = pipeline.dependencies_satisfied
            self.assertTrue(res)

    def test_save(self):
        self._test_save()


if __name__ == '__main__':
    main()
