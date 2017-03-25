# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html



# import pymongo
#
# class MongoPipeline(object):
#
#     collection_name = 'Jobs'
#
#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongodb://db.localhost:27017/KnockerDB;
#         self.mongo_db = mongo_db
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get('MONGO_URI'),
#             mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
#         )
#
#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#
#     def close_spider(self, spider):
#         self.client.close()
#
#     def process_item(self, item, spider):
#         self.db[self.collection_name].insert(dict(item))
#         return item
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

class KnockerPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True;
        for data in item:
            # if not data:
            #     valid = False
            #     raise DropItem("Missing {0}!".format(data))
            # if valid:
            #     self.collection.insert(dict(item))
            #     log.msg("Question added to MongoDB database!",
            #             level=log.DEBUG, spider=spider)
            if not data:
                raise DropItem("Missing data!")
                self.collection.update({'url': item['url']}, dict(item), upsert=True)
                log.msg("items added",
                level=log.DEBUG, spider=spider)
        return item
