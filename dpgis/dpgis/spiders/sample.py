"""
PROJECT summary_: We have a rest api. we are going to try it out to see the outcome. 
"""  
      """
USING SCRAPY FRAMEWORK TO EXTRACT FEATURECLASS FROM A MAPSERVICE
"""
# import sys
# import os
# #importing libraries
# from typing import Any, Iterable
# import scrapy
# from scrapy.http import Response
# import scrapy.http
# from working.items import WorkingItem
# from scrapy_playwright.page import PageMethod

# # #Initiating class
# # class SampleSpider(scrapy.Spider):
# #     name = 'sample'
# #     # start_url = ['https://maps.dggs.alaska.gov/gmc/search#q=core&page=0'
# #     #              ]
    
# #     def start_requests(self):
# #         #url = 'https://maps.dggs.alaska.gov/gmc/js/search.js'
# #         url = 'https://maps.dggs.alaska.gov/gmc/search#q=core&page=0'
        
# #         yield scrapy.Request(
# #             url, 
# #             meta= dict(
# #                 playwright = True,
# #                 playwright_include_page = True,
# #                 errback = self.errback,
# #             ),
# #         )
        
# #     async def parse(self, response):
# #         sample = response.meta["playwright_page"]
# #         content = await sample.content()
# #         await sample.close()
        
# #         response = scrapy.http.TextResponse(
# #             url = response.url,
# #             body = content,
# #             encoding = 'utf-8'
# #         )
        
# #         # for sa in response.css('div.table.tbody.tr.outcrop'):
# #         #     sa = WorkingItem(
# #         #         ID = sa.css('.td:nth-child(1).a ::text').get(),  
# #         #         Related = sa.css('.td:nth-child(2).div ::text').get() ,	
# #         #         Sample_Slide = sa.css('.td:nth-child(3) ::text').get() , 
# #         #         Box_Set = sa.css('.td:nth-child(4) ::text').get(),
# #         #         Core_No_Diameter = sa.css('.td:nth-child(5)::text').get(),
# #         #         Top_Bottom = sa.css('td:nth-child(6)::text').get(),
# #         #         Keywords = sa.css('td:nth-child(7).ul.kw.li ::text').get(),
# #         #         Collection = sa.css('td:nth-child(8) ::text').get(),  
# #         #     )
# #         for sa in response.css('div.table.tbody.tr.outcrop'):
# #             item = {
# #                 'ID': sa.css('.td:nth-child(1).a ::text').get(),  
# #                 'Related': sa.css('.td:nth-child(2).div ::text').get(),  
# #                 'Sample_Slide': sa.css('.td:nth-child(3) ::text').get(),  
# #                 'Box_Set': sa.css('.td:nth-child(4) ::text').get(),
# #                 'Core_No_Diameter': sa.css('.td:nth-child(5)::text').get(),
# #                 'Top_Bottom': sa.css('td:nth-child(6)::text').get(),
# #                 'Keywords': sa.css('td:nth-child(7).ul.kw.li ::text').get(),
# #                 'Collection': sa.css('td:nth-child(8) ::text').get(),  
# #             }
            
# #             yield sa
            
# #     async def errback(self, failure):
# #         sample = failure.request.meta['playwright_page']
# #         await sample.close()
    
    
# # class SampleSpider(scrapy.Spider):
# #     name = 'sample'
# #     start_urls = ['https://maps.dggs.alaska.gov/gmc/search#q=core&page=0']

#     # def parse(self, response):
#     #     # Extract the URL of the CSV file
#     #     csv_url = response.css('a#csv::attr(href)').get()
#     #     if csv_url:
#     #         yield scrapy.Request(
#     #             url=response.urljoin(csv_url),
#     #             callback=self.save_csv
#     #         )

#     # def save_csv(self, response):
#     #     # Save the CSV file
#     #     file_name = 'downloaded_file.csv'
#     #     with open(file_name, 'wb') as f:
#     #         f.write(response.body)
#     #     self.log(f'CSV file saved as {file_name}')
    

        
# #We are going to retry the original script and try and study the pagination
# import scrapy
# import json 
# # https://maps.dggs.alaska.gov/gmc/search.json

# #--------ALASKA
# class SampleSpider(scrapy.Spider):
#     name = "sample"
#     start_urls = ['https://maps.dggs.alaska.gov/gmc/search.json']

#     custom_settings = {
#         'FEEDS': {
#             'output.json': {
#                 'format': 'json',
#                 'encoding': 'utf8',
#                 'store_empty': False,
#                 'indent': 4,
#             },
#         },
#     }

#     def parse(self, response):
#         data = json.loads(response.body)
#         num_found = data.get('numFound', 0) #numfound is at the root level of the json structure
#         docs = data.get('docs', [])
#         start = data.get('start', 0)
        
#         #doc is
#         response_data = data.get('response', {})

#         # Yield each document found
#         for doc in docs:
#             yield self.flatten_nested_dict(doc)

#         next_start = start + len(docs)
#         if next_start < num_found:
#             next_url = f'https://maps.dggs.alaska.gov/gmc/search.json?start={next_start}&rows=1000'  
#             headers = {
#                 'Referer': 'https://maps.dggs.alaska.gov/gmc/search#q=core&page=0' 
#             }
#             yield scrapy.Request(url=next_url, headers=headers, callback=self.parse)
            
#     def start_requests(self):
#         initial_url = "https://maps.dggs.alaska.gov/gmc/search.json?start=0&rows=1000"
#         headers = {
#             'Referer': 'https://maps.dggs.alaska.gov/gmc/search#q=core&page=0'
#         }
#         yield scrapy.Request(url=initial_url, headers=headers, callback=self.parse)
        
#     def flatten_nested_dict(self, d, parent_key='', sep='_'):
#         """
#         Flattens a nested dictionary.
#         """
#         items = []
#         for k, v in d.items():
#             new_key = f"{parent_key}{sep}{k}" if parent_key else k
#             if isinstance(v, dict):
#                 items.extend(self.flatten_nested_dict(v, new_key, sep=sep).items())
#             elif isinstance(v, list):
#                 for i, item in enumerate(v):
#                     if isinstance(item, dict):
#                         items.extend(self.flatten_nested_dict(item, f"{new_key}{sep}{i}", sep=sep).items())
#                     else:
#                         items.append((f"{new_key}{sep}{i}", item))
#             else:
#                 items.append((new_key, v))
#         return dict(items)