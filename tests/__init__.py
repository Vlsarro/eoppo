import os
import pickle
from unittest import TestCase, mock
from eippm.exceptions import EIPPMSaveException


class EIPPMBaseTestCase(TestCase):

    def setUp(self) -> None:
        super(EIPPMBaseTestCase, self).setUp()
        self.test_module_filepath = os.path.join(os.path.dirname(__file__), 'test_module')
        self.test_dependencies = ('numpy', 'pillow')

    def tearDown(self) -> None:
        super(EIPPMBaseTestCase, self).tearDown()
        self._remove_saved_module()

    def _remove_saved_module(self):
        try:
            os.remove(self.test_module_filepath)
        except OSError:
            pass

    def create_default_test_obj(self):
        raise NotImplementedError()

    def _test_save(self):
        m = self.create_default_test_obj()
        m.save(self.test_module_filepath)

        with open(self.test_module_filepath, 'rb') as f:
            loaded_m = pickle.load(f)

        self.assertEqual(m.__dict__, loaded_m.__dict__)

        with mock.patch('pickle.dump') as mock_dump:
            mock_dump.side_effect = [TypeError('err')]

            with self.assertRaises(EIPPMSaveException) as cm:
                m.save(self.test_module_filepath)

            self.assertIsInstance(cm.exception.cause, TypeError)
