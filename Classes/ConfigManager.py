import configparser


class Singleton(object):
    _instance = None
    def __new__(class_, path, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance


class ConfigManager(Singleton):
    def __init__(self, path):
        self.config = configparser.ConfigParser()
        self.config.read(path)

    def get(self, field, section='DEFAULT'):
        return self.config[section][field]