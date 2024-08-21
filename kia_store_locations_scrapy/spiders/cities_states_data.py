import json
from typing import Iterable
import scrapy
from scrapy import Request
from scrapy.cmdline import execute

from kia_store_locations_scrapy.items import StatesAndCitiesItem


class CitiesStatesDataSpider(scrapy.Spider):
    name = "cities_states_data"
    allowed_domains = ["kia.com"]

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.kia.com/api/kia2_in/findAdealer.getStateCity.do',
            method='POST'
        )

    def parse(self, response, **kwargs):
        item = StatesAndCitiesItem()
        raw_data = json.loads(response.body)
        for data in raw_data['data']['stateAndCity']:
            item['state_name'] = data['val1']['value']
            item['state_key'] = data['val1']['key']
            for city_data in data['val2']:
                item['city_name'] = city_data['value']
                item['city_key'] = city_data['key']
                yield item


if __name__ == '__main__':
    execute('scrapy crawl cities_states_data'.split())
