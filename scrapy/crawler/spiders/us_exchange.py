# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy.exceptions import CloseSpider


class USExchangeSpider(scrapy.Spider):
    name = 'us-exchange'
    allowed_domains = ['finance.daum.net']
    start_urls = ['https://finance.daum.net/']
    base_url = 'https://finance.daum.net/api/exchanges/FRX.KRWUSD/days?symbolCode=FRX.KRWUSD&terms=days&page={}&perPage=30'
    referer = 'https://finance.daum.net/exchanges/FRX.KRWUSD'

    def start_requests(self):
        first_page = 1
        request_url = self.base_url.format(first_page)
        yield scrapy.Request(url=request_url, callback=self.parse, meta={'page': 1, 'total_pages': None},
                             headers={'referer': self.referer})

    def parse(self, response):
        if response.meta['total_pages'] == response.meta['page']:
            raise CloseSpider('Reached to the last page: %d' % response.meta['page'])

        try:
            data = json.loads(response.body)
            total_pages = data['totalPages']
            for datum in data['data']:
                yield USExchangeSpider.clean_data(datum)
        except ValueError:
            raise CloseSpider('No proper data: %s' % response.url)

        next_page = response.meta['page'] + 1
        next_url = self.base_url.format(next_page)

        yield scrapy.Request(url=next_url, callback=self.parse, meta={'page': next_page, 'total_pages': total_pages},
                             headers={'referer': self.referer, })

    @staticmethod
    def clean_data(datum):
        sign = 1
        if datum['change'] == 'FALL':
            sign = -1

        return {
            'date': datum['date'][0:10],
            'price': datum['basePrice'],
            'change_price': sign * datum['changePrice'],
            'change_rate': sign * datum['changeRate'],
            'cash_buy_price': datum['cashBuyingPrice'],
            'cash_sell_price': datum['cashSellingPrice'],
            'transfer_buy_price': datum['ttBuyingPrice'],
            'transfer_sell_price': datum['ttSellingPrice'],
            'exchange_commission': datum['exchangeCommission'],
            'us_dollar_rate': datum['usDollarRate']
        }


