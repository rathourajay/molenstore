# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class DprtmntScrapeItem(Item):
    # define the fields for your item here like:
    # name = Field()
    localid = Field()
    url = Field()
    name = Field()
    description = Field()
    price = Field()
    image_urls = Field()
    image_alts = Field()
    images = Field()
    stock = Field()
    stock_available = Field()
    category_string = Field()
    designer_string  = Field()
    currency = Field()
    sale_price = Field()
    pass
