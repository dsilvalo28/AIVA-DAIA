from src import TreeDetector
from src import utils
import unittest
import os
import cv2
import numpy as np

constant_percentage = [0.25, 0.75]
constant_m2 = [80, 100]
constant_n_trees = [200, 300]
constant_coordinates_low = [45, -90]
constant_coordinates_high = [46, -91]

max_overlapping = 0.05

test_path = "images/test/"
gt_buildings_path = "building_gt/"


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.detector = TreeDetector.Detector()

    # def setUp(self):
    #     print('Init test')

    def test_get_map_image(self):
        map_image = utils.get_map_image(constant_coordinates_low, constant_coordinates_high)
        self.assertGreater(np.sum(map_image), 0)

    def test_overlapping(self):
        '''

        Test for checking overlapping between segmented trees and buildings
        '''
        path_images = os.listdir(test_path)
        for path in path_images:
            if path.endswith(".tif"):
                self.detector.read(test_path + path)
                segmentation = self.detector.process_image()
                building_map = cv2.imread(test_path + gt_buildings_path + path)
                building_segmentation = cv2.cvtColor(building_map, cv2.COLOR_BGR2GRAY).astype(np.bool)
                overlapping = np.logical_and(segmentation, building_segmentation)
                self.assertLess(np.mean(overlapping), max_overlapping)

    def test_percentage(self):
        """
        Test for checking the percentage of tree mass
        """
        path_images = os.listdir(test_path)
        for path in path_images:
            if path.endswith(".tif"):
                self.detector.read(test_path + path)
                percentage = self.detector.calculate_percentage()
                self.assertGreater(percentage, constant_percentage[0])
                self.assertLess(percentage, constant_percentage[1])

    def test_m2(self):
        """
        Test for checking the area of tree mass
        """
        path_images = os.listdir(test_path)
        for path in path_images:
            if path.endswith(".tif"):
                self.detector.read(test_path + path)
                m2 = self.detector.calculate_m2()
                self.assertGreater(m2, constant_m2[0])
                self.assertLess(m2, constant_m2[1])

    def test_number_trees(self):
        """
        Test for checking the number of trees
        """
        path_images = os.listdir(test_path)
        for path in path_images:
            if path.endswith(".tif"):
                self.detector.read(test_path + path)
                n_trees = self.detector.calculate_number_trees()
                self.assertGreater(n_trees, constant_n_trees[0])
                self.assertLess(n_trees, constant_n_trees[1])


if __name__ == '__main__':
    # Test sets
    test_results = unittest.TestSuite()
    test_results.addTest(Test('test_percentage'))
    test_results.addTest(Test('test_m2'))
    test_results.addTest(Test('test_number_trees'))

    # Test launch
    # unittest.TextTestRunner().run(test_results)
    unittest.main()
