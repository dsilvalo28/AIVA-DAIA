from src import TreeDetector
import unittest
import os
import cv2


constant_percentage = 0.75
constant_km2 = 80
constant_n_trees = 100
path = "C:/Users/dsilvalo/PycharmProjects/AIVA-DAIA/images_test/"


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.detector = TreeDetector.Detector()
        print('Init class')

    def setUp(self):
        print('Init test')

    def test_percentage(self):
        """
        Test for checking the percentage of tree mass
        """
        images = os.listdir(path)
        for img in images:
            i = cv2.imread(path + img)
            percentage = self.detector.calculate_percentage(i)

        self.assertGreater(percentage, constant_percentage)

    def test_m2(self):
        """
        Test for checking the area of tree mass
        """
        images = os.listdir(path)
        for img in images:
            i = cv2.imread(path + img)
            m2 = self.detector.calculate_m2(i)

        self.assertGreater(m2, constant_km2)

    def test_numer_trees(self):
        """
        Test for checking the number of trees
        """
        images = os.listdir(path)
        for img in images:
            i = cv2.imread(path + img)
            n_trees = self.detector.calculate_numer_trees(i)

        self.assertGreater(n_trees, constant_n_trees)


if __name__ == '__main__':
    # Test sets
    tests1 = unittest.TestSuite()
    tests1.addTest(Test('test_rectangle'))

    # Test launch
    # unittest.TextTestRunner().run(tests1)
    unittest.main()
