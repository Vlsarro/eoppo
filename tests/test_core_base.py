import pkg_resources
from typing import Callable
from unittest import main, mock

from tests import EIPPMBaseTestCase
from eippm.core.base import BaseImageProcessingModule
from eippm.exceptions import (EIPPMInitializationException, EIPPMUnhandledException, EIPPMNotInitializedException,
                              EIPPMDependenciesNotSatisfiedException)


sample_callback_data = {'a': 5, 'b': 4, 'data': {'a': 5}}


class TestImageProcessingModule(BaseImageProcessingModule):
    _version = (0, 0, 1, 'alpha', 0)

    def _process(self, image, callback: Callable = None, **kwargs):
        if callback:
            callback(**sample_callback_data)
        return image


class BaseImageProcessingModuleTests(EIPPMBaseTestCase):

    def create_default_test_obj(self):
        return TestImageProcessingModule(auto_init=False)

    @mock.patch('pkg_resources.require')
    def test_module_initialize(self, mock_require):
        m = self.create_default_test_obj()
        m._dependencies = self.test_dependencies

        mock_require.side_effect = [pkg_resources.VersionConflict(), True]

        with self.assertRaises(EIPPMDependenciesNotSatisfiedException):
            m.initialize()

        self.assertFalse(m.is_initialized)

        m._dependencies_satisfied = None

        with mock.patch.object(m, '_initialize') as mock_initialize:
            mock_initialize.side_effect = [ValueError()]
            with self.assertRaises(EIPPMInitializationException) as cm:
                m.initialize()

        self.assertIsInstance(cm.exception.cause, ValueError)
        self.assertFalse(m.is_initialized)

        m.initialize()
        self.assertTrue(m.is_initialized)

    def test_module_process(self):
        m = self.create_default_test_obj()

        test_arg = [1, 2, 3]

        with self.assertRaises(EIPPMNotInitializedException):
            m.process(None)

        m.initialize()

        with mock.patch.object(m, '_process') as mock_process:
            sample_result = [22, 322, 322]

            mock_process.side_effect = [ValueError(), sample_result, ValueError()]

            with self.assertRaises(EIPPMUnhandledException) as cm:
                m.process(None)

            self.assertIsInstance(cm.exception.cause, ValueError)

            out = m.process(None)
            self.assertEqual(sample_result, out)

            m.ignore_processing_errors = True

            out = m.process(test_arg)
            self.assertEqual(test_arg, out)

        callback_result = []
        out = m.process(test_arg, callback=lambda **kwargs: callback_result.append(kwargs))
        self.assertEqual(test_arg, out)
        self.assertEqual(1, len(callback_result))
        self.assertDictEqual(callback_result[0], sample_callback_data)

    def test_module_mixin_props(self):
        m = self.create_default_test_obj()

        with mock.patch('pkg_resources.require') as mock_require:
            res = m.dependencies_satisfied
            self.assertTrue(res)

            m._dependencies = self.test_dependencies
            mock_require.side_effect = [pkg_resources.VersionConflict(), None]

            m._dependencies_satisfied = None
            res = m.dependencies_satisfied
            self.assertFalse(res)

            m._dependencies_satisfied = None
            res = m.dependencies_satisfied
            self.assertTrue(res)

        self.assertEqual('0.0.1', m.version)

        self.assertEqual('TestImageProcessingModule (0.0.1)', m.full_name)
        self.assertEqual('TestImageProcessingModule', m.short_name)

        self.assertFalse(m.is_initialized)

        m.initialize()
        self.assertTrue(m.is_initialized)

    def test_save(self):
        self._test_save()


if __name__ == '__main__':
    main()
