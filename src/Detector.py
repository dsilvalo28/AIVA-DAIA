from abc import abstractmethod
from abc import ABC


class Detector(ABC):
    def __init__(self, image=None):
        pass

    @abstractmethod
    def read(self, image):
        pass

    @abstractmethod
    def process_image(self):
        pass
