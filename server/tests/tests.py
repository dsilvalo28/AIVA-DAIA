from src.TreeDetector import TreeDetector
from src.MapReading import MapReader
import src.utils as utils
import unittest
import os
import cv2
import numpy as np

constant_percentage = [0.01, 0.1]
constant_m2 = [200, 2000]
constant_n_trees = [200, 1000]
max_overlapping = 0.001

test_path = "images/test/"
gt_buildings_path = "building_gt/"
address = 'URJC Mostoles'
coordinates = [30.223423, -97.782728]
import matplotlib.pyplot as plt


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.TD = TreeDetector()
        cls.MR = MapReader()
        cls.debug = False
        if 'DEBUG' in os.environ:
            cls.debug = os.environ['DEBUG']

    # def setUp(self):
    #     print('Init test')

    def test_get_map_image(self):
        map_image_coord = self.MR.get_by_coordinates(coordinates, resolution=[1000, 1000])
        self.assertGreater(np.sum(map_image_coord), 0)
        map_image_zone = self.MR.get_by_zone(address, resolution=[1000, 1000])
        self.assertGreater(np.sum(map_image_zone), 0)
        if self.debug == 'True':
            plt.figure()
            plt.ion()
            plt.imshow(map_image_coord)
            plt.title('Map image by coordinates: {}'.format(str(coordinates)))
            plt.show()

            plt.figure()
            plt.ion()
            plt.imshow(map_image_zone)
            plt.title('Map image by zone: {}'.format(str(address)))
            plt.show()

    def test_overlapping(self):
        '''

        Test for checking overlapping between segmented trees and buildings
        '''
        path_images = os.listdir(test_path)
        for path in path_images:
            if path.endswith(".tif"):
                img = self.TD.read_from_path(test_path + path)
                segmentation = self.TD.process_image()
                segmentation_bw = cv2.cvtColor(segmentation, cv2.COLOR_BGR2GRAY).astype(
                    np.bool)
                building_segmentation = cv2.imread(test_path + gt_buildings_path + path)
                building_segmentation_bw = cv2.cvtColor(building_segmentation, cv2.COLOR_BGR2GRAY).astype(np.bool)
                overlapping = np.logical_and(segmentation_bw, building_segmentation_bw)
                self.assertLess(np.mean(overlapping), max_overlapping)
                if self.debug == 'True':
                    overlay = (np.bitwise_and(building_segmentation, segmentation).astype(np.float) * np.array(
                        [[[1, 0, 0]]], dtype=np.float)).astype(
                        np.uint8)
                    result = cv2.addWeighted(src1=img, alpha=1, src2=overlay, beta=1, gamma=0)
                    plt.figure()
                    plt.ion()
                    plt.imshow(result)
                    plt.title('Overlapping')
                    plt.show()

    def test_percentage(self):
        """
        Test for checking the percentage of tree mass
        """
        path_images = os.listdir(test_path)
        for path in path_images:
            if path.endswith(".tif"):
                self.TD.read_from_path(test_path + path)
                percentage = self.TD.calculate_percentage()
                self.assertGreater(percentage, constant_percentage[0])
                self.assertLess(percentage, constant_percentage[1])

    def test_m2(self):
        """
        Test for checking the area of tree mass
        """
        path_images = os.listdir(test_path)
        for path in path_images:
            if path.endswith(".tif"):
                self.TD.read_from_path(test_path + path)
                m2 = self.TD.calculate_m2()
                self.assertGreater(m2, constant_m2[0])
                self.assertLess(m2, constant_m2[1])

    def test_number_trees(self):
        """
        Test for checking the number of trees
        """
        path_images = os.listdir(test_path)
        for path in path_images:
            if path.endswith(".tif"):
                self.TD.read_from_path(test_path + path)
                n_trees = self.TD.calculate_number_trees()
                self.assertGreater(n_trees, constant_n_trees[0])
                self.assertLess(n_trees, constant_n_trees[1])

    @classmethod
    def tearDownClass(cls):
        if cls.debug == 'True':
            print("WIP: Might be unstable")
            input("Press any key")  # Might be unstable


if __name__ == '__main__':
    # Test sets
    test_results = unittest.TestSuite()
    test_results.addTest(Test('test_percentage'))
    test_results.addTest(Test('test_m2'))
    test_results.addTest(Test('test_number_trees'))

    # Test launch
    # unittest.TextTestRunner().run(test_results)
    unittest.main()
