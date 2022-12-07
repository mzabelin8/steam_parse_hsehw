# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GameItems(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    category = scrapy.Field()
    reviews = scrapy.Field()
    rating = scrapy.Field()
    release = scrapy.Field()
    developer = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    platforms = scrapy.Field()
