# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html



import pymongo
from scrapy.conf import settings
from scrapy import log


class MongoPipeline(object):
    def __init__(self):
        self.connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.db = self.connection[settings['MONGODB_DB']]
        self.collection = self.db[settings['MONGODB_COLLECTION']]

    def open_spider(self, spider):
        self.crawl = self.db[settings['CRAWL_COLLECTION']]
        self.crawl_id_one = self.crawl.find_one()['crawl_id']
        self.crawl_id = self.crawl_id_one + 1

    def process_item(self, item, spider):
        item['crawl_id'] = self.crawl_id
        self.collection.replace_one({'url': item['url']}, dict(item), upsert=True)
        log.msg("items added",
                level=log.DEBUG, spider=spider)

    def close_spider(self, spider):
        self.crawl.replace_one({'crawl_id': self.crawl_id_one}, {'crawl_id': self.crawl_id})
        self.connection.close()
