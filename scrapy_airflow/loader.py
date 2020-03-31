# -*- coding: utf-8 -*-
import os
import glob
import scrapy
import inspect
import importlib
from scrapy_airflow.config import ConfigLoader
from scrapy.crawler import CrawlerProcess


class SpiderLoader:

    @staticmethod
    def get_spider(spider_name):
        """This function get a spider module from the given directory in scrapy-airflow.cfg

        :param spider_name: spider script name or spider name
        :return: spider module object
        """
        config_loader = ConfigLoader()
        spider_root = config_loader['spider_path']
        spider_path = os.path.join(spider_root, spider_name)
        spider_module = SpiderLoader.module_loader(spider_path)
        return spider_module

    @staticmethod
    def module_loader(py_dir):
        """This finds a .py in a given directory;
        a multiple files with the same name would result in the first one found

        :param py_dir: an absolute path directory where a module is located
        """
        importlib.import_module(py_dir)
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


def runner(spider):
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'items.json'
    })

    process.crawl(spider)
    process.start()

import json

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
from scrapy_airflow.scrapy.crawler.spiders.us_exchange import *

class MyPipeline(object):
    def process_item(self, item, spider):
        results.append(dict(item))

results = []
def spider_closed(spider):
    print(results)

# set up spider
spider = USExchangeSpider()

# set up settings
settings = get_project_settings()
settings.overrides['ITEM_PIPELINES'] = {'__main__.MyPipeline': 1}

# set up crawler
crawler = Crawler(settings)
crawler.signals.connect(spider_closed, signal=signals.spider_closed)
crawler.configure()
crawler.crawl(spider)

# start crawling
crawler.start()
log.start()
reactor.run()