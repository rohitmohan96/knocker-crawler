# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class CategoryItem(Item):
    title = Field()
    url = Field()


class JobItem(Item):
    title = Field()
    id = Field()
    skills = Field()
    experience = Field()
    location = Field()
    education = Field()
    url = Field()
