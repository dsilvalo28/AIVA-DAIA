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
        self.__totalm2 = 12000
        self.__treesperm2 = 0.6

    # *** PRIVATE *** #
    def __preprocess_image(self):
        """
        :return: Preprocessed set image
        """
        preprocessed_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

        return preprocessed_image, hsv_image

    # *** PUBLIC *** #
    def read(self, image):
        """
        :param image: Set the image to work with
        """
        self.image = image

    def read_from_path(self, image_path):
        """
        :param image_path: Set the path to read the image and the image
        """
        self.__image_path = image_path
        self.image = cv2.imread(self.__image_path)
        return self.image

    def process_image(self, lc=[0, 100, 100], uc=[120, 255, 255]):
        """
        :param lc: [int, int, int] Lower HSV color values
        :param uc: [int, int, int] Lower HSV color values
        :return: [np.array] 3 channel segmentation mask of the set image
        """
        preprocessed_image, hsv_image = self.__preprocess_image()
        ret, segmented_image = cv2.threshold(preprocessed_image, self.__threshold_down, self.__threshold_up,
                                             cv2.THRESH_BINARY)

        # Creaccion de mascara
        lower_color = np.array(lc, dtype='uint8')
        upper_color = np.array(uc, dtype='uint8')
        mask = cv2.inRange(hsv_image, lower_color, upper_color)
        mask_3_channels = np.dstack((mask, mask, mask))

        # ret2, thresh = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # segmented_image_boolean = segmented_image.astype(np.bool)
        return mask_3_channels

    def calculate_percentage(self):
        """
        :return: Percentage of tree mass of the set image
        """
        segmented_image = self.process_image()
        percentage = np.mean(segmented_image/2.55)
        return percentage

    def calculate_m2(self):
        """
        :return: m² of tree mass of the set image
        """
        percentage = self.calculate_percentage()
        m2 = percentage * self.__totalm2
        return m2

    def calculate_number_trees(self):
        """
        :return: Number of trees of the set image
        """
        m2 = self.calculate_m2()
        n_trees = int(m2 * self.__treesperm2)
        return n_trees
