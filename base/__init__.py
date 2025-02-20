import logging

class GlobalLogger:
    def __init__(self, name="global_logger", level=logging.INFO):
        self.logger = logging.getLogger(name)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.setLevel(level)
        self.logger.addHandler(handler)

def get_global_logger():
    return GlobalLogger().logger

global_logger = get_global_logger()

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls in cls._instances:
            raise Exception(f"This class is a singleton! Instance of {cls.__name__} already exists.")
        instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
        cls._instances[cls] = instance
        return instance