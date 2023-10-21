import scrapy
from scrapy.crawler import CrawlerProcess
from itertools import zip_longest
import pandas as pd
from urls import start_urls

class DynamicScraper(scrapy.Spider):
    name = 'dynamic_scraper'

    # To store data from all pages
    all_data = {}

    def start_requests(self):
        urls = start_urls  # Make sure to replace this with your URL list
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = {}

        item['title'] = response.xpath('.//div[@class="breadcrumbs noprint"]//text()').extract()
        item['description'] = response.xpath('.//span[@itemprop="name"]//text()').extract()
        item['page_link'] = response.url

        # Handling dynamic headings
        headings = response.xpath('.//div[@class="product_info_filters"]//ul[@class="product_info_filters"]/li/strong | //div[@class="product_info_filters"]//ul[@class="product_info_filters"]/li/sub').extract()
        values = response.xpath('.//div[@class="product_info_filters"]//ul[@class="product_info_filters"]/li/text()').extract()

        for h, v in zip_longest(headings, values, fillvalue=None):
            item[h] = v

        # Save the item data to the all_data dictionary
        self.all_data[response.url] = item

    def close(self, reason):
        # When spider finishes, convert dictionary to DataFrame and save to CSV
        df = pd.DataFrame(self.all_data).T
        df.to_csv('output.csv', index=False)

process = CrawlerProcess()
process.crawl(DynamicScraper)
process.start()