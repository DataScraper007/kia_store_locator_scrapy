# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StatesAndCitiesItem(scrapy.Item):
    state_name = scrapy.Field()
    state_key = scrapy.Field()
    city_name = scrapy.Field()
    city_key = scrapy.Field()

class StoreDetailsItem(scrapy.Item):
    dealer_name = scrapy.Field()
    address1 = scrapy.Field()
    address2 = scrapy.Field()
    address3 = scrapy.Field()
    website = scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()
    phone1 = scrapy.Field()
    phone2 = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    dealer_type = scrapy.Field()
    email = scrapy.Field()
    page_url = scrapy.Field()

