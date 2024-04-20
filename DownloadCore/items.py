# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RrysItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    video_ts = scrapy.Field()

class BilibiliItem(scrapy.Item):
    title = scrapy.Field()
    audio = scrapy.Field()
    video = scrapy.Field()
    
class IyhdmmItem(scrapy.Item):
    title = scrapy.Field()
    video_ts = scrapy.Field()