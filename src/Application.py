import matplotlib.pyplot as plt
from src.MapReading import MapReader
from src.TreeDetector import TreeDetector
from src.utils import save_image as save_image
import numpy as np
import cv2
import sys


# Tree detector class #
class Application:
    def __init__(self):
        self.MR = MapReader()
        self.TD = TreeDetector()

        self.__map = None
        self.__mask = None
        self.__result = None
        self.__percentage = None
        self.__m2 = None
        self.__n = None

        # *** CONSTANTS *** #
        self.__save_test_name = 'test_map'
        self.__save_mask_name = 'mask'
        self.__save_mixed_name = 'result'
        self.__lc = [50, 10, 30]
        self.__uc = [90, 90, 90]
        self.__mix_color = [0.0, 1.0, 0.0]

        # self.run(address='Austin, Texas')
        # self.run(coordinates=[30.223423, -97.782728])
        self.run(image_path='images/test/austin1.tif')

    # *** PUBLIC *** #
    def run(self, address=None, coordinates=None, image_path=None):
        """
        :param address: [str] User input to get image by address
        :param coordinates: [float, float] User input to get image by coordinates
        :param image_path: [str] User input to get image by path
        :return: Shows result processed image
        """
        if address is not None:
            self.__map = self.MR.get_by_zone(address)
            self.TD.read(self.__map)
        elif coordinates is not None:
            self.__map = self.MR.get_by_coordinates(coordinates)
            self.TD.read(self.__map)
        elif image_path is not None:
            self.__map = self.TD.read_from_path(image_path)
        else:
            print('Define run input')
            sys.exit(1)
        self.__mask = self.TD.process_image(self.__lc, self.__uc)
        overlay = (self.__mask.astype(np.float) * np.array([[self.__mix_color]], dtype=np.float)).astype(np.uint8)
        self.__result = cv2.addWeighted(src1=self.__map, alpha=1, src2=overlay, beta=0.6, gamma=0, dst=self.__result)
        self.__percentage = self.TD.calculate_percentage()
        self.__m2 = self.TD.calculate_m2()
        self.__n = self.TD.calculate_number_trees()
        self.show_result()

    def show_map(self):
        plt.figure()
        plt.ion()
        plt.imshow(self.__map)
        plt.title('Percentage of tree mass: {:.3f}% m2: {:.0f} m2 Number of trees: {} trees'.format(self.__percentage,
                                                                                                    self.__m2,
                                                                                                    self.__n))
        plt.show()

    def show_mask(self):
        plt.figure()
        plt.ion()
        plt.imshow(self.__mask)
        plt.title('Percentage of tree mass: {:.3f}% m2: {:.0f} m2 Number of trees: {} trees'.format(self.__percentage,
                                                                                                    self.__m2,
                                                                                                    self.__n))
        plt.show()

    def show_result(self):
        plt.figure()
        plt.ion()
        plt.imshow(self.__result)
        plt.title('Percentage of tree mass: {:.3f}% m2: {:.0f} m2 Number of trees: {} trees'.format(self.__percentage,
                                                                                                    self.__m2,
                                                                                                    self.__n))
        plt.show()

    def save_map(self):
        save_image(self.__save_test_name, self.__map)

    def save_mask(self):
        save_image(self.__save_mask_name, self.__mask)

    def save_result(self):
        save_image(self.__save_mixed_name, self.__result)


if __name__ == '__main__':
    app = Application()
    input("Press any key")
