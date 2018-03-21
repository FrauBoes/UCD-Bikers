import unittest

import bikers


class BikersTestCase(unittest.TestCase):

    def setUp(self):
        self.app = bikers.app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertIn('Welcome to UCD-Bikers', rv.data.decode())


if __name__ == '__main__':
    unittest.main()
