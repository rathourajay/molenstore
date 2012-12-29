# -*- coding: cp1252 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item
import urllib2
from dprtmnt_scrape.items import DprtmntScrapeItem
import re

class moltenstore_com(CrawlSpider):
    name = "moltenstore_com"
    DOWNLOAD_DELAY = 2
    COOKIES_ENABLED = False
    USER_AGENT = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
    allowed_domains = ["moltenstore.com"]
    start_urls = [
        "http://www.moltenstore.com/" 
    ]

    rules =   (
                Rule(SgmlLinkExtractor(allow=['/categories/']), callback='parse_item', follow=True),
                Rule(SgmlLinkExtractor(allow=[r'/categories.php\?category=']), callback='parse_item', follow=True),
                Rule(SgmlLinkExtractor(allow=[r'/products.php\?product=']), callback='parse_item', follow=True),
		
                )

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)
        
        item = DprtmntScrapeItem()

        item['localid'] = []

        item['url'] = response.url

        item['name'] = hxs.select('//h1/following-sibling::h2[1]/text()').extract()

        item['description'] = hxs.select('//section[@id = "ProductDescription"]').extract()
        
        item['image_urls'] = hxs.select('//img[contains(@id,"TinyImage")]/@src | //img[contains(@src,"std.jpg")]/@src').extract()

        for sale_price in  hxs.select('substring-after(//span[@class = "SalePrice"]/text(), "$")').extract():
            if sale_price:
                item['sale_price'] = hxs.select('substring-after(//span[@class = "SalePrice"]/text(), "$")').extract()
            else:
                item['price'] = hxs.select('substring-after(//em[contains(@class,"ProductPrice")]/text(), "$")').extract()

        item['image_alts'] = hxs.select('//img[contains(@id,"TinyImage")]/@alt | //img[contains(@src,"std.jpg")]/@alt').extract()
           
        for data in hxs.select('//em[contains(@class,"ProductPrice")]/text() | //span[@class = "SalePrice"]/text()').extract():
            if '$' in data:
                item['currency'] = '$'

        page = urllib2.urlopen(response.url).read()
        page_without_newline = page.replace('\n','').replace('\r','').replace('\t','')
        if 'var invLevel =' in page_without_newline:
            avail = page_without_newline.split('var invLevel =')[1].split(';')[0].strip()
            if 'sold out' not in avail.lower():
                item['stock_available'] = avail
                item['stock'] = "True"
            else:
                item['stock'] = "False"  
                
        else:
            item['stock'] = "-3"

        designers = ['Archie Grand','Cori Umi','Demeter','Estell','Fieldguided','House of Harlow','Megan Todd','LAS','Low Luv',"Millimeter-Milligram MMMG","Molten Relic",'O-Check','Pigeonhole','Rachel Pfeffer x Molten Store','Rosebud Perfume Co.']
        
        for desginer in designers:
            if desginer in page_without_newline:
                item['designer_string'] = desginer
          

        #determine categories
        url = response.url 
 
        if 'Necklace' in url:
            item['category_string'] = "Necklaces"        

        elif 'Earrings' in url:
            item['category_string'] = "Earrings"

        elif 'Ring' in url:
            item['category_string'] = "Rings"

        elif 'Notebook' in url:
            item['category_string'] = "Stationary"

        elif 'Book' in url: 
            item['category_string'] = "Stationary"

        elif '-Print' in url:
            item['category_string'] = "Stationary"

        elif '-Card' in url:
            item['category_string'] = "Stationary"

        elif 'Journal' in url:
            item['category_string'] = "Stationary"

        elif '-Candle' in url:
            item['category_string'] = "Stationary"

        elif '-Vase' in url:
            item['category_string'] = "Stationary"

        elif '-Board' in url:
            item['category_string'] = "Stationary"

        elif '-Bag' in url:
            item['category_string'] = "Stationary"

        elif '-Diary' in url:
            item['category_string'] = "Stationary"

        else:
            item['category_string'] = "no category"
        
        if item['name'] == []:
            return None 
        else: 
            self.log('This is an item page: %s' % response.url)
            return item
