import unittest

from eippm.core.base import BaseImageProcessingModule


class TestImageProcessingModule(BaseImageProcessingModule):
    _version = (0, 0, 1, 'alpha', 0)


class BaseImageProcessingModuleTests(unittest.TestCase):

    def test_module_init(self):
        m = TestImageProcessingModule()
        self.assertFalse(m.is_initialized)

        m.initialize()
        self.assertTrue(m.is_initialized)

    def test_module_mixin_props(self):
        m = TestImageProcessingModule()

        self.assertEqual('0.0.1', m.version)
        self.assertEqual('TestImageProcessingModule_v0.0.1', m.name)


if __name__ == '__main__':
    unittest.main()
