import scrapy
import pymongo
from pymongo import MongoClient
import constant
client = MongoClient(constant.mongoUrl)
db = client.cryptocurrency
currency = db.currency
import datetime

class coinDetailScrapper(scrapy.Spider):
    name = "coinDetailScrapper"
    start_urls = ['https://coinmarketcap.com/coins/views/all/']
    def parse(self, response):
        SET_SELECTOR = '.js-summary-table tbody tr'
        for coin in response.css(SET_SELECTOR):
            temp = {
                'id': coin.css('td ::text').extract_first(),
                'name': coin.css('.currency-name a.currency-name-container ::attr(href)').extract_first().split('/')[2],
                'symbol': coin.css('.col-symbol ::text').extract_first(),
                'marketCap': coin.css('.market-cap ::text').extract_first(),
                'priceBTC': coin.css('td a.price ::attr(data-btc)').extract_first(),
                'priceUSD': coin.css('td a.price ::attr(data-usd)').extract_first(),
                'circulatingSupply': coin.css('a ::attr(data-supply)').extract_first(),
                'volume24h': coin.css('td a.volume  ::attr(data-usd)').extract_first(),
                'change1h': coin.css('.percent-1h ::attr(data-usd)').extract_first(),
                'change24h': coin.css('.percent-24h ::attr(data-usd)').extract_first(),
                'change7d': coin.css('.percent-7d ::attr(data-usd)').extract_first(),
                'createdAt': datetime.datetime.utcnow(),
                'isDeleted': False
            }
            currency.insert_one(temp)

