"""
PROJECT summary_:  The goal of this task is to extract both Feature Classes and other aspatial dataset to enable some data science 
investigation on air quality in the USA. I are utilising the RESTAPI which I had to find from map service site for AirNOW, a site that
provides data for air quality around the USA.  https://www.airnow.gov/  
"""  

#importing libraries
import sys
import os
import json 
import pandas as pd
import glob
import csv
import requests


#STEP 1
#define url variable
url = 'https://www.arcgis.com/sharing/rest/content/items/92e772c4f65a4848a29bcc24c8f61bab/data?f=json'
response = requests.get(url)
if response.status_code == 200:
    json_response = response.json()
    data = json_response['operationalLayers'] #[2]['url']
    with open('output1.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    print("JSON file has been created.")
    
    #to csv - a little effort
    headers = ['id', 'url', 'visibility', 'opacity', 'title', 'itemId', 'type', 'layerType', 'visibleFolders']
    with open('filtered_output.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        # Write the headers (specified keys)
        writer.writeheader()
        
        # Write rows by extracting only the desired keys from each object
        for layer in data:
            # Create a filtered dictionary with only the desired keys
            filtered_layer = {key: layer.get(key) for key in headers}
            writer.writerow(filtered_layer)
    
    print("CSV file has been created with the specified keys.")
  
  
  
""" Step ONE of parent data file is complete. Now I will into the parent file to
extract specific data most important to the objective of the investigation. 

I will access the data in each service layer and post it to a repository 
with which I will be  able to explore and analyse it. Hence STEP 2 in AirNow2.py 
"""

#---------------------NEXT IS AirNow2.py-----------------------