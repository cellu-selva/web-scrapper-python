"""
high level support for doing this and that.
"""
import datetime
import time
import scrapy
from pymongo import MongoClient
import constant

client = MongoClient(constant.mongoUrl)
db = client.cryptocurrency
currency = db.currency
currencyHistory = db.currencyHistory
count = 0
urls = []

class currencyHistoryScrapper(scrapy.Spider):

    name = "currencyHistoryScrapper"
    for coin in currency.find():
        urls.append({
            'url': 'https://coinmarketcap.com/currencies/'+  coin.get('name')
                   +'/historical-data/?start=20130428&end=20171105',
            'coin': coin.get('name')
        })
    start_urls = [urls[0].get('url')]
    currentCurrency = urls[0].get('coin')
    def parse(self, response):
        for history in response.css('.table-responsive tbody tr'):
            temp = {
                'date': history.css('td:nth-child(n+1)::text').extract_first(),
                'open': history.css('td:nth-child(n+2)::text').extract_first(),
                'high': history.css('td:nth-child(n+3)::text').extract_first(),
                'low': history.css('td:nth-child(n+4)::text').extract_first(),
                'close': history.css('td:nth-child(n+5)::text').extract_first(),
                'volume': history.css('td:nth-child(n+6)::text').extract_first(),
                'marketCap': history.css('td:nth-child(n+7)::text').extract_first(),
                'name': self.currentCurrency,
                'createdAt': datetime.datetime.utcnow(),
                'isDeleted': False
            }
            currencyHistory.insert_one(temp)
        global count
        count += 1
        if len(urls) > count:
            self.currentCurrency = urls[count].get('coin')
            time.sleep(6)
            yield scrapy.Request(urls[count].get('url'), callback=self.parse)
