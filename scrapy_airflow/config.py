import os
import configparser
from collections import OrderedDict


CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'scrapy-airflow.cfg')


class Config(object):
    """Singleton pattern config loader;
    Once the object is created, it will reuse the same setting!
    """

    config = None

    def __new__(cls):
        if cls.config is None:
            cls.config = object.__new__(cls)
        return cls.config

    def __init__(self):
        if not CONFIG_FILE:
            print('The path of config file is not specified!')
        else:
            try:
                self._load_config(CONFIG_FILE)
            except FileNotFoundError:
                print('Config file %s does not exist!' % CONFIG_FILE)

    def _load_config(self, filename):
        """Load config file and store them into dictionary

        :param filename: config file path
        :return: It returns a dict where key is config name, values are dict
        """
        self.config = OrderedDict()
        config = configparser.ConfigParser()
        config.read(filename)
        config_keys = config.sections()

        for key in config_keys:
            setting = OrderedDict()
            for field in config.items(key):
                # ConfigParser loads settings in the form of tuple
                # This will add them into the dictionary
                setting[field[0]] = field[1]
            self.config[key] = setting
