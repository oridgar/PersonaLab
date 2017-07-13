import unittest

class Test1(unittest.TestCase):
    def test_upper(self):
        self.assertEqual("FOO","FOO")