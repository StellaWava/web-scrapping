import scrapy


class SampleSpider(scrapy.Spider):
    name = "sample"
    allowed_domains = ["sample.com"]
    start_urls = ["https://sample.com"]

    def parse(self, response):
        pass
