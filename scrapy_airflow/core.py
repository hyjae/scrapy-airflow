import os
import glob
import scrapy
import inspect
import importlib
from scrapy_airflow.config import Config
from scrapy.crawler import CrawlerProcess


class SpiderLoader:
    spiders = None

    @classmethod
    def get_spiders(cls):
        cur_path = os.path.dirname(__file__)
        spider_dir = os.path.join(cur_path, 'spiders')
        config_dir = os.path.join(cur_path, 'config.cfg')

        cls.spiders = cls.module_loader(spider_dir)

        for key, value in cls.spiders.items():
            "By default, each spider dict has keys 'spider' and 'args'"
            cls.spiders[key] = dict({'spider': cls.spiders[key]})
            cls.spiders[key]['args'] = list()
        for key, value in Config().config.items():
            if key in cls.spiders:
                cls.spiders[key].update(cls.set_args())
        return cls.spiders
    #
    # @staticmethod
    # def set_args():
    #     """Read all values from config and set as a dict in each spider instance"""
    #     result = dict()
    #     for key, value in Config().config.items():
    #         if key == 'args':
    #             file_path = os.path.join(os.path.join(os.path.dirname(__file__), 'files'))
    #             file_path = os.path.join(file_path, value)
    #             logger.info('Read args from %s' % file_path)
    #             result[key] = utils.parse_csv(file_path)
    #         else:
    #             result[key] = value
    #     return result

    @staticmethod
    def module_loader(dir):
        """This finds a .py in a given directory;
        a multiple files with the same name would result in the first one found

        :param dir: an absolute path directory where a module is located
        """
        modules = dict()
        package = 'scrapy.crawler.spiders'

        config_loader = Config()
        config_loader.config

        for file in glob.glob(os.path.join(dir, '*.py')):
            name = os.path.splitext(os.path.basename(file))[0]
            if name.startswith('_'):
                continue
            module = importlib.import_module('.'+name, package=package)
            # member == classname
            for member in dir(module):
                "Return only classes that have the same name as filenames"
                if member.lower() == name:
                    handler_class = getattr(module, member)
                    if handler_class and inspect.isclass(handler_class):
                        modules[name] = handler_class
        return modules


class MySpider(scrapy.Spider):
    # Your spider definition
    ...


process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': 'items.json'
})

process.crawl(MySpider)
process.start()
