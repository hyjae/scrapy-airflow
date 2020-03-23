import json
import scrapy


class InvestingSpider(scrapy.Spider):
    name = 'investing'
    start_urls = ['https://sbcharts.investing.com/charts_xml/c4caa3c525726eb96b6ee67ddfa57896_max.json',  # Crude Oil WTI
                  'https://sbcharts.investing.com/charts_xml/1a5f95b308e1d982eec66b97f9895bac_max.json',  # S&P 500 Futures
                  'https://sbcharts.investing.com/charts_xml/052c52690818141ba55d9f690f97cf96_max.json',  # US Wheat Futures
                  'https://sbcharts.investing.com/charts_xml/91b94ebf1783b56de4050ca5a85a2cb6_max.json',  # US Soybeans Futures
                  'https://sbcharts.investing.com/charts_xml/5b7f484afa4efd7da6890d631ce8afc4_max.json',  # Copper Futures
                  'https://sbcharts.investing.com/charts_xml/c4651fb6e12fa8166f3d0af875aede53_max.json',  # Silver Futures
                  'https://sbcharts.investing.com/charts_xml/d565a7612f2d571d32033540114babb3_max.json']  # Gold Futures
    allowed_domains = ['sbcharts.investing.com']
    filter_urls = []

    def parse(self, response):
        try:
            content = response.body.decode('utf-8')
            data = json.loads(content)
            data['url'] = response.url
            yield data
        except ValueError:
            self.logger.info('Error occured during requesting %s' % response.url)
