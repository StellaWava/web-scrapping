
""" Step TWO of parent data file is complete. Now I will into the parent file to
extract specific data most important to the objective of the investigation. 

I will access the data in each service layer and post it to a repository 
with which I will be  able to explore and analyse it. Hence STEP 2 in sample_scrapy2.py 
"""
#importing libraries
import sys
import os
import json 
import pandas as pd
import glob
import csv
import requests

#STEP 2
#NOTE**we could link the script to the previous but not now.
#instead ingest the file from our storage folder
data_file = pd.read_csv('filtered_output.csv')

# Define indexes of interest for demo
indexes = [2, 6,9,15,33,60] #, 8, 11, 17, 35, 62
#select important rows
selected_rows = data_file.loc[indexes, ['id', 'url']]

#loop through each index record to fetch the url
for _, row in selected_rows.iterrows():
    file_id = row['id']
    base_url = row['url']
    #define the supported operation to extract data
    query_url = f"{base_url}/query"
    
    #set parameters of interes
    params = {
        'where': '1=1',           # Retrieve all records
        'outFields': '*',          # Get all fields
        'f': 'json',               # Specify output format as JSON
        'returnGeometry': 'true'   # Return geometries
    }
    
    #make request
    response = requests.get(query_url, params=params)
    if response.status_code == 200:
        json_data = response.json()  # Parse the JSON response
        
        #save files by id name
        output_file = f"{file_id}.json"
        with open(output_file, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        print(f"JSON file has been created: {output_file}")
    else:
        print(f"Failed to retrieve data for ID {file_id}: {response.status_code}")
        
   
"""
Dependig on available company resources or tech stacks, we could store that data on cloud either as a filetype 
or SQL db since it is relational data. However, we can also extract it to csv or explore it in JSON format, 
for more data science work. 
For explicity of the task, I will go ahead and extract one of the JOSN FeatureClass to csv in the 
highlighted script below.
"""

# #---------------------------------------
# with open('Air_Now_Site_Data_3485_3372.json') as f:
#     data = json.load(f)

# # Open a CSV file to write to
# with open('Air_Now_Site_Data_3485_3372.csv', mode='w', newline='') as file:
#     # Get field names from the first feature's attributes and add 'x' and 'y' for geometry
#     fieldnames = list(data['features'][0]['attributes'].keys()) + ['x', 'y']
    
#     # Set up the CSV writer with the fieldnames as headers
#     writer = csv.DictWriter(file, fieldnames=fieldnames)
    
#     # Write headers
#     writer.writeheader()
    
#     # Write rows for each feature
#     for feature in data['features']:
#         # Start with the attribute data
#         row = feature['attributes'].copy()
        
#         # Add geometry data
#         row['x'] = feature['geometry']['x']
#         row['y'] = feature['geometry']['y']
        
#         # Write the row to the CSV file
#         writer.writerow(row)
# print("CSV file has been created: Air_Now_Monitors_Ozon.csv")

#-----------------------------------END------------------------------------