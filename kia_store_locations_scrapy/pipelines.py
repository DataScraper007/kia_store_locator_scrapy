# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
from mysql.connector import Error


class BasePipeline():

    def __init__(self):
        self.conn = None
        self.cur = None

    def open_spider(self, spider):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                database='kia_scrapy',
                user='root',
                password='actowiz',
                autocommit=True
            )
            self.cur = self.conn.cursor()
        except Error as e:
            spider.logger.error(f"Error connecting to MySQL: {e}")

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()


class KiaStoreLocationsScrapyPipeline(BasePipeline):
    def process_item(self, item, spider):
        query= """insert into kia_scrapy.store_data (dealer_name, address1, address2, address3, website, lng, lat, phone1, phone2,
                   city, state, dealer_type, email, page_url) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
        values = (
            item['dealer_name'],
            item['address1'],
            item['address2'],
            item['address3'],
            item['website'],
            item['lng'],
            item['lat'],
            item['phone1'],
            item['phone2'],
            item['city'],
            item['state'],
            item['dealer_type'],
            item['email'],
            item['page_url']
        )
        self.cur.execute(query, values)


class StatesAndCitiesPipeline(BasePipeline):
    def process_item(self, item, spider):
        query = """insert into kia_scrapy.states_and_cities (state_name, state_key, city_name, city_key) 
                    values (%s,%s,%s,%s);"""
        values = (item['state_name'], item['state_key'], item['city_name'], item['city_key'])
        self.cur.execute(query, values)

