import pkg_resources
from unittest import mock, main
from typing import Callable, Any
from tests import EIPPMBaseTestCase
from eippm.core.base import BaseImageProcessingModule
from eippm.core.pipeline import ImageProcessingModulesPipeline


class TestModule1(BaseImageProcessingModule):
    def _process(self, image: Any, callback: Callable = None, **kwargs) -> Any:
        return image + 5


class TestModule2(BaseImageProcessingModule):
    def _process(self, image: Any, callback: Callable = None, **kwargs) -> Any:
        return image + 6


class TestModule3(BaseImageProcessingModule):
    def _process(self, image: Any, callback: Callable = None, **kwargs) -> Any:
        return image + 7


class TestImageProcessingModulesPipeline(ImageProcessingModulesPipeline):
    _version = (0, 0, 1, 'alpha', 0)


class ImageProcessingModulesPipelineTests(EIPPMBaseTestCase):

    def create_default_test_obj(self):
        return TestImageProcessingModulesPipeline([])

    def test_run(self):
        pipeline = TestImageProcessingModulesPipeline([TestModule1(), TestModule2(), TestModule3()])
        result = pipeline.run(0)
        self.assertEqual(18, result)

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
