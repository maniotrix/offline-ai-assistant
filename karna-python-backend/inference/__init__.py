from abc import ABC
import logging


class BaseInference(ABC):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        pass