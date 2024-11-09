"""
USING SCRAPY FRAMEWORK TO EXTRACT FEATURECLASS FROM A MAPSERVICE
"""
import sys
import os
import json 
from typing import Any, Iterable
import scrapy
from scrapy.http import Response
import scrapy.http
from working.items import WorkingItem
from scrapy_playwright.page import PageMethod

#Initiating class
class SampleSpider(scrapy.Spider):
    name = 'sample'
    start_url = ['https://insert_name/gmc/search#q=core&page=0'
                 ]
    
    def start_requests(self):
        #url = 'https://insert_name/gmc/js/search.js'
        url = 'https://insert_name/gmc/search#q=core&page=0'
        
        yield scrapy.Request(
            url, 
            meta= dict(
                playwright = True,
                playwright_include_page = True,
                errback = self.errback,
            ),
        )
        
    async def parse(self, response):
        sample = response.meta["playwright_page"]
        content = await sample.content()
        await sample.close()
        
        response = scrapy.http.TextResponse(
            url = response.url,
            body = content,
            encoding = 'utf-8'
        )
        
        for sa in response.css('div.table.tbody.tr.outcrop'):
            item = {
                'ID': sa.css('.td:nth-child(1).a ::text').get(),  
                'Related': sa.css('.td:nth-child(2).div ::text').get(),  
                'Sample_Slide': sa.css('.td:nth-child(3) ::text').get(),  
                'Box_Set': sa.css('.td:nth-child(4) ::text').get(),
                'Core_No_Diameter': sa.css('.td:nth-child(5)::text').get(),
                'Top_Bottom': sa.css('td:nth-child(6)::text').get(),
                'Keywords': sa.css('td:nth-child(7).ul.kw.li ::text').get(),
                'Collection': sa.css('td:nth-child(8) ::text').get(),  
            }
            
            yield sa
            
    async def errback(self, failure):
        sample = failure.request.meta['playwright_page']
        await sample.close()

    

        
"""
#PAGINATED SITE

class SampleSpider(scrapy.Spider):
    name = "sample"
    start_urls = ['https://maps.dggs.alaska.gov/gmc/search.json']

    custom_settings = {
        'FEEDS': {
            'output.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'indent': 4,
            },
        },
    }

    def parse(self, response):
        data = json.loads(response.body)
        num_found = data.get('numFound', 0) #numfound is at the root level of the json structure
        docs = data.get('docs', [])
        start = data.get('start', 0)
        
        #doc is
        response_data = data.get('response', {})

        # Yield each document found
        for doc in docs:
            yield self.flatten_nested_dict(doc)

        next_start = start + len(docs)
        if next_start < num_found:
            next_url = f'https://insert_name/gmc/search.json?start={next_start}&rows=1000'  
            headers = {
                'Referer': 'https://inser_name/gmc/search#q=core&page=0' 
            }
            yield scrapy.Request(url=next_url, headers=headers, callback=self.parse)
            
    def start_requests(self):
        initial_url = "https://insert_name/gmc/search.json?start=0&rows=1000"
        headers = {
            'Referer': 'https://insert_name/gmc/search#q=core&page=0'
        }
        yield scrapy.Request(url=initial_url, headers=headers, callback=self.parse)
        
    def flatten_nested_dict(self, d, parent_key='', sep='_'):
        #Flattens a nested dictionary.
      
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flatten_nested_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        items.extend(self.flatten_nested_dict(item, f"{new_key}{sep}{i}", sep=sep).items())
                    else:
                        items.append((f"{new_key}{sep}{i}", item))
            else:
                items.append((new_key, v))
        return dict(items)

""" 