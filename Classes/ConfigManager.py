import configparser


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ConfigManager(metaclass = Singleton):
    def __init__(self, path=None):
        self.config = configparser.ConfigParser()
        self.config.read(path)

    def get(self, field, section='DEFAULT'):
        return self.config[section][field]
