import cv2
import numpy as np


# Helpful functions #
def get_map_image(max_coordinates, min_coordinates):
    return np.zeros((1000, 1000, 3))