from .context import src
import unittest


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Init class')

    def setUp(self):
        print('Init test')

    def test_1(self):
        print('Test 1')

if __name__ == '__main__':
    # Test sets
    tests1 = unittest.TestSuite()
    tests1.addTest(Test('test_1'))

    # Test launch
    # unittest.TextTestRunner().run(tests1)
    unittest.main()
