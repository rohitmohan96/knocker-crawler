# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class JobItem(Item):
    title = Field()
    skills = Field()
    experience = Field()
    location = Field()
    education = Field()
    url = Field()
