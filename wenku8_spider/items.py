# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    book_id = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    last_update = scrapy.Field()
    content_original_url = scrapy.Field()
    content_url = scrapy.Field()
    pass
