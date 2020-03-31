# -*- coding: utf-8 -*-
import os
import random
import logging
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

logger = logging.getLogger(__name__)
USER_AGENTS_FILE = os.path.join(os.path.join(os.path.dirname(__file__), 'files'), 'useragents.txt')


class RandomUserAgentMiddleware(UserAgentMiddleware):
    """This middleware allows you to rotate user-agent info each time you send a request
    """

    def __init__(self, settings, user_agent='default'):
        super(RandomUserAgentMiddleware, self).__init__()
        try:  # get user-agents from file
            with open(USER_AGENTS_FILE, 'r') as f:
                logger.info('A user-agent file has been loaded!')
                self.user_agent_list = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            # get user_agents from settings.py
            logger.error('%s does not exist!' % USER_AGENTS_FILE)
            ua = settings.get('USER_AGENT', user_agent)
            self.user_agent_list = [ua]

    @classmethod
    def from_crawler(cls, crawler):
        obj = cls(crawler.settings)
        crawler.signals.connect(obj.spider_opened, signal=signals.spider_opened)
        return obj

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agent_list)
        if user_agent:
            request.headers.setdefault('User-Agent', user_agent)
