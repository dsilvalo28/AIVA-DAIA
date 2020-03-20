import cv2
import numpy as np
from src.Detector import Detector


# Tree detector class #
class TreeDetector(Detector):
    def __init__(self, image_path=None):
        self.__image_path = image_path
        self.image = None
        if image_path is not None:
            self.read(self.__image_path)

        # *** CONSTANTS *** #
        self.__threshold_down = 127
        self.__threshold_up = 255
        self.__totalm2 = 1200

    # *** PRIVATE *** #
    def __preprocess_image(self):
        preprocessed_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

        return preprocessed_image, hsv_image

    # *** PUBLIC *** #
    def read(self, image_path):
        self.__image_path = image_path
        self.image = cv2.imread(self.__image_path)

    def process_image(self):
        preprocessed_image, hsv_image = self.__preprocess_image()
        ret, segmented_image = cv2.threshold(preprocessed_image, self.__threshold_down, self.__threshold_up,
                                             cv2.THRESH_BINARY)

        # Creaccion de mascara
        lower_color = np.array([0, 100, 100], dtype='uint8')
        upper_color = np.array([120, 255, 255], dtype='uint8')
        mask = cv2.inRange(hsv_image, lower_color, upper_color)

        # ret2, thresh = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        segmented_image_boolean = segmented_image.astype(np.bool)
        return mask

    def calculate_percentage(self):
        segmented_image = self.process_image()
        percentage = np.mean(segmented_image)
        return percentage

    def calculate_m2(self):
        percentage = self.calculate_percentage()
        m2 = percentage * self.__totalm2
        return m2

    def calculate_number_trees(self):
        segmented_image = self.process_image()
        n_trees = 120
        return n_trees
