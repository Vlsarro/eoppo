import pkg_resources
from unittest import mock, main
from typing import Callable, Any

from tests import EIPPMBaseTestCase
from eippm.core.base import BaseImageProcessingModule
from eippm.core.pipeline import ImageProcessingModulesPipeline
from eippm.exceptions import EIPPMUnhandledException


class TestModule1(BaseImageProcessingModule):
    callback_msg = 'TestModule1 called'

    def _process(self, image: Any, callback: Callable = None, **kwargs) -> Any:
        if callback:
            callback(data=self.callback_msg)
        return image + 5


class TestModule2(BaseImageProcessingModule):
    callback_msg = 'TestModule2 called'

    def _process(self, image: Any, callback: Callable = None, extra_num=0, **kwargs) -> Any:
        if callback:
            callback(data=self.callback_msg)
        return image + 6 + extra_num


class TestModule3(BaseImageProcessingModule):
    callback_msg = 'TestModule3 called'

    def _process(self, image: Any, callback: Callable = None, extra_num=0, **kwargs) -> Any:
        if callback:
            callback(data=self.callback_msg)
        return image + 7 + extra_num


class TestModule4(TestModule3):

    def process(self, image: Any, callback: Callable[..., None] = None, **kwargs) -> Any:
        raise ValueError('test error')


class TestImageProcessingModulesPipeline(ImageProcessingModulesPipeline):
    _version = (0, 0, 1, 'alpha', 0)


class ImageProcessingModulesPipelineTests(EIPPMBaseTestCase):

    def create_default_test_obj(self):
        return TestImageProcessingModulesPipeline([])

    def test_run_simple(self):
        pipeline = TestImageProcessingModulesPipeline([TestModule1(), TestModule2(), TestModule3()])
        result = pipeline.run(0)
        self.assertEqual(18, result)

    def test_run_unhandled_error(self):
        pipeline = TestImageProcessingModulesPipeline([TestModule1(), TestModule4()])
        with self.assertRaises(EIPPMUnhandledException) as cm:
            pipeline.run(0)
        self.assertIsInstance(cm.exception.cause, ValueError)

    def test_run_processing_error(self):
        pipeline = TestImageProcessingModulesPipeline([TestModule1(), TestModule3()])
        with self.assertRaises(EIPPMUnhandledException) as cm:
            pipeline.run(0, call_params={
                1: {
                    'params': {
                        'extra_num': 'not_an_integer'
                    }
                }
            })
        self.assertIsInstance(cm.exception.cause, TypeError)

    def test_run_unhandled_error_ignore(self):
        pipeline = TestImageProcessingModulesPipeline([TestModule1(), TestModule4()], ignore_processing_errors=True)
        result = pipeline.run(0)
        self.assertEqual(5, result)

    def test_run_processing_error_ignore(self):
        pipeline = TestImageProcessingModulesPipeline([TestModule1(), TestModule3()], ignore_processing_errors=True)
        result = pipeline.run(0, call_params={
            1: {
                'params': {
                    'extra_num': 'not_an_integer'
                }
            }
        })
        self.assertEqual(5, result)

    def test_run_call_params(self):
        m1 = TestModule1()
        m2 = TestModule2()
        m3 = TestModule3()

        pipeline = TestImageProcessingModulesPipeline([m1, m2, m3])

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
        with self.assertRaises(EIPPMUnhandledException) as cm:
            pipeline.run(0, call_params=call_params)

        self.assertIsInstance(cm.exception.cause, TypeError)

        call_params[2]['exc_to_ignore'] = (TypeError,)

        result = pipeline.run(0, call_params=call_params)
        self.assertEqual(16, result)

    def test_run_call_params_invalid_idx(self):
        pipeline = TestImageProcessingModulesPipeline([TestModule1(), TestModule3()])
        result = pipeline.run(0, call_params={325435: {}})
        self.assertEqual(12, result)

    def test_pipeline_props(self):
        m1 = TestModule1(auto_init=False)
        m2 = TestModule2(auto_init=False)
        m3 = TestModule3()

        pipeline = TestImageProcessingModulesPipeline([m1, m2, m3])
        self.assertFalse(pipeline.is_initialized)

        m1.initialize()
        m2.initialize()
        self.assertTrue(pipeline.is_initialized)

        self.assertEqual('0.0.1', pipeline.version)

        self.assertEqual('TestImageProcessingModulesPipeline (0.0.1)', pipeline.full_name)
        self.assertEqual('TestImageProcessingModulesPipeline', pipeline.short_name)

        with mock.patch('pkg_resources.require') as mock_require:
            res = pipeline.dependencies_satisfied
            self.assertTrue(res)

            m4 = TestModule3(auto_init=False)
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
