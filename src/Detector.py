from abc import abstractmethod
from abc import ABC


class Detector(ABC):
    def __init__(self, image_path=None):
        pass

    @abstractmethod
    def read(self, image_path):
        pass

    @abstractmethod
    def process_image(self):
        pass
