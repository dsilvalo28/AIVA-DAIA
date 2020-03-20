import matplotlib.pyplot as plt
import src.MapReader as MapReader
import src.TreeDetector as TreeDetector
from src.utils import save_image as save_image


# Tree detector class #
class Application:
    def __init__(self):
        self.MR = MapReader()
        self.TD = TreeDetector()

        self.__map = None
        self.__mask = None
        self.__result = None

        # *** INPUTS *** #
        self.address = 'Austin, Texas'
        self.coordinates = [30.223423, -97.782728]
        self.uc = [120, 255, 255]
        self.lc = [0, 100, 100]

        # *** CONSTANTS *** #
        self.__save_test_name = 'test_map'
        self.__save_mask_name = 'mask'
        self.__save_mixed_name = 'result'

        self.run()

    # *** PUBLIC *** #
    def run(self):
        map = self.MR.get_by_coordinates(self.__coordinates)
        save_image(self.__save_test_name, map)

    def show_map(self):
        print('WIP')

    def show_mask(self):
        print('WIP')

    def show_result(self):
        print('WIP')

    def save_map(self):
        print('WIP')

    def save_mask(self):
        print('WIP')

    def save_result(self):
        print('WIP')
