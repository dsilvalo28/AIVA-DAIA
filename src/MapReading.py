import cv2
import numpy as np


# Tree detector class #
class MapReader:
    def __init__(self, resolution=None):
        if resolution is None:
            resolution = (5000, 5000)
        self.__resolution = resolution

    # *** PUBLIC *** #
    def get_by_coordinates(self, coordinates):
        image = np.ones(self.__resolution)
        return image

    def get_by_zone(self, zone):
        zone_coordinates = []
        image = self.get_by_coordinates(zone_coordinates)
        return image

    def config(self, resolution):
        self.__resolution = resolution
