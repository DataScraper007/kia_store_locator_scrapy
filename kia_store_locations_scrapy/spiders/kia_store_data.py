import html
import json
from typing import Iterable
import scrapy
from scrapy import Request
import mysql.connector
from scrapy.cmdline import execute

from kia_store_locations_scrapy.items import StoreDetailsItem


class KiaStoreDataSpider(scrapy.Spider):
    name = "kia_store_data"
    allowed_domains = ["kia.com"]
    start_urls = ["https://kia.com"]

    def __init__(self, ):
        super().__init__()
        self.city_key = None
        self.state_key = None

    def start_requests(self):
        conn = mysql.connector.connect(
            host='localhost',
            database='kia_scrapy',
            user='root',
            password='actowiz',
            autocommit=True
        )
        cur = conn.cursor()
        cur.execute('select * from states_and_cities')
        rows = cur.fetchall()
        for row in rows:
            self.state_key = row[2]
            self.city_key = row[4]
            payload = {
                'state': row[2],
                'city': row[4],
                'dealerType': 'A'
            }

            yield scrapy.FormRequest(
                url='https://www.kia.com/api/kia2_in/findAdealer.getDealerList.do',
                method='POST',
                formdata=payload,
                callback=self.parse,
            )

    def check_keys(self, data):
        keys = ['dealerName', 'address1', 'address2', 'address3', 'website', 'lng', 'lat', 'phone1', 'phone2',
                'cityName', 'stateName', 'dealerType', 'email']
        for key in keys:
            if key not in data:
                data[key] = 'NA'
        return data

    def parse(self, response, **kwargs):
        item = StoreDetailsItem()
        raw_data = json.loads(response.body.decode('utf-8'))

        for data in raw_data['data']:
            data = self.check_keys(data)
            item['dealer_name'] = data['dealerName'].strip()
            item['address1'] = data['address1'].strip()
            item['address2'] = data['address2'].strip()
            item['address3'] = data['address3'].strip()
            item['website'] = data['website']
            item['lng'] = data['lng']
            item['lat'] = data['lat']
            item['phone1'] = data['phone1']
            item['phone2'] = data['phone2']
            item['city'] = data['cityName']
            item['state'] = data['stateName']
            item['dealer_type'] = data['dealerType']
            item['email'] = data['email']
            item['page_url'] = f"https://www.kia.com/in/buy/find-a-dealer/result.html?state={self.state_key}&city={self.city_key}"
            yield item


if __name__ == '__main__':
    execute('scrapy crawl kia_store_data'.split())
