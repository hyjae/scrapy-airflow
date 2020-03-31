import os
import scrapy
import importlib
import scrapy.signals
from scrapy.crawler import CrawlerProcess
from config import ConfigLoader


class SpiderLoader:

    @staticmethod
    def get_spider(spider_name):
        """This function get a spider module from the given directory in scrapy-airflow.cfg

        :param spider_name: spider script name or spider name
        :return: spider module object
        """
        config_loader = ConfigLoader()
        spider_root = config_loader.get_setting('spider_path')
        spider_path = os.path.join(spider_root, spider_name)
        spider_module = SpiderLoader.module_loader(spider_path)
        return spider_module

    @staticmethod
    def module_loader(py_dir):
        """This finds a .py in a given directory;
        a multiple files with the same name would result in the first one found

        :param py_dir: an absolute path directory where a module is located
        """

        return importlib.import_module(py_dir)
        # getattr(module)

        # package = 'scrapy.crawler.spiders'
        #
        # config_loader = ConfigLoader()
        # config_loader.config
        #
        # for file in glob.glob(os.path.join(py_dir, '*.py')):
        #     name = os.path.splitext(os.path.basename(file))[0]
        #     if name.startswith('_'):
        #         continue
        #     module = importlib.import_module('.'+name, package=package)
        #     # member == classname
        #     for member in py_dir(module):
        #         "Return only classes that have the same name as filenames"
        #         if member.lower() == name:
        #             handler_class = getattr(module, member)
        #             if handler_class and inspect.isclass(handler_class):
        #                 modules[name] = handler_class
        # return modules


class ScrapyRunner:

    def __init__(self, spider_module):
        self.result = []
        self.spider_module = spider_module
        self.process = CrawlerProcess()

    def _spider_closed(self, spider):
        stat = spider.crawler.stats._stats
        if 'log_count/ERROR' in stat.keys():
            self.result.append(True)
        self.result.append(False)

    def run_process(self):
        self.process.crawl(self.spider_module)
        for p in self.process.crawlers:
            p.signals.connect(self._spider_closed, signal=scrapy.signals.spider_closed)
        self.process.start()
        return self.result
