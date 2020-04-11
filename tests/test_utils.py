from eoppo.utils.version import get_version
import unittest


class UtilsTests(unittest.TestCase):

    def test_get_version(self):
        v = (0, 0, 1, 'alpha', 0)
        result = get_version(v)
        self.assertEqual('0.0.1', result)


if __name__ == '__main__':
    unittest.main()
