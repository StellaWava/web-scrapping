"""
PROJECT summary_: We have a rest api. we are going to try it out to see the outcome. 
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
# url = 'https://www.arcgis.com/sharing/rest/content/items/92e772c4f65a4848a29bcc24c8f61bab/data?f=json'
# response = requests.get(url)
# #print(response)
# if response.status_code == 200:
#     #print(response.headers)
#     #print(response.content)
#     json_response = response.json()
#     data = json_response['operationalLayers'] #[2]['url']
    # for v in data[0]:
    #     #return keys of object 1
    #     print(v)
    #     #return values of object 1
    #     #m = data[0][v]
    #     #print(v, m)
    
    # #return all values for a given nested key
    # for v in data:
    #     n = v['url']
    #     print(n)
    
    # #return all objects in the array
    # for index, layer in enumerate(data):
    #     print(f"Object {index + 1}:")
        
    #     for key, value in layer.items():
    #         print(f"{key}: {value}")
    #     #draw separator. 
    #     print("-" * 40)
    
    # # #now improve the data to go to a csv/ json file
    # with open('output1.json', 'w') as json_file:
    #     json.dump(data, json_file, indent=4)
    
    # print("JSON file has been created.")
    
    # #to csv - a little effort
    # headers = ['id', 'url', 'visibility', 'opacity', 'title', 'itemId', 'type', 'layerType', 'visibleFolders']
    # with open('filtered_output.csv', mode='w', newline='') as file:
    #     writer = csv.DictWriter(file, fieldnames=headers)
    #     # Write the headers (specified keys)
    #     writer.writeheader()
        
    #     # Write rows by extracting only the desired keys from each object
    #     for layer in data:
    #         # Create a filtered dictionary with only the desired keys
    #         filtered_layer = {key: layer.get(key) for key in headers}
    #         writer.writerow(filtered_layer)
    
    # print("CSV file has been created with the specified keys.")
    

#STEP 2, We need to access the data in each service layer and post it to a repository with which we will be able to explore and analyse it.
# #extract data from the urls
# #air_now file link
# query_url_air = 'https://services.arcgis.com/cJ9YHowT8TU7DUyn/arcgis/rest/services/Air_Now_Monitors_Ozone/FeatureServer/0/query'
# params = {
#     'where': '1=1',          # Query condition (returns all records)
#     'outFields': '*',         # Get all fields
#     'f': 'json',              # Specify output format as JSON
#     'returnGeometry': 'true'  # Return geometries
# }
# response = requests.get(query_url_air, params=params)
# if response.status_code == 200:
#     json_data = response.json()  # Parse the JSON response
    
#     # Save the raw JSON data to a file
#     with open('Air_Now_Monitors_Ozone.json', 'w') as json_file:
#         json.dump(json_data, json_file, indent=4)
    
#     print("JSON file has been created: Air_Now_Monitors_Ozone.json")
# else:
#     print(f"Failed to retrieve data: {response.status_code}")

#STEP 3:
# #CONVERTING THE JSON TO CSV FOR DS & ESDA  - Keeping the assumption that you do not have arcGIS licence  
# data_source = 'Air_Now_Monitors_Ozone.json'
# with open(data_source) as f:
#     data = json.load(f)

# # Open a CSV file to write to
# with open('Air_Now_Monitors_Ozone.csv', mode='w', newline='') as file:
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



#Now write a script for all the links in the json/csv file. 
"""_summary_: Since this only a project demonstration, fetching all the data is not valuable so we focus on fetching only the critical files
that will fit one or two of our data science and analysis critical questions. 
Here, I went ahead and performed a review of the filtered_output files that we have at hand. --Preferably, df.loc['url', axis 
Note** 
- Review data file and establish the supported format and supported operations of the files. These assist in optimization of your approach
- For training purposes, we are simply extracting all the data but noteworthy, the supported operations include Query, Filter, and Select and 
that means that we can apply any of these specifics in our workflow. Since the goal is general data processing. 

"""


#air_now file link
#we could link the script to the previous but not now.
data_file = pd.read_csv('filtered_output.csv')

# Define indexes of interest for demo
indexes = [2, 6,9,15,33,60] #, 8, 11, 17, 35, 62
#select important rows
selected_rows = data_file.loc[indexes, ['id', 'url']]

#loop through each index record to fetch the url
for _, row in selected_rows.iterrows():
    file_id = row['id']
    query_url = row['url']
    
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
        output_file = f"{file_id}_Air_Now_Monitors_Ozone.json"
        with open(output_file, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        print(f"JSON file has been created: {output_file}")
    else:
        print(f"Failed to retrieve data for ID {file_id}: {response.status_code}")
        
"""Dependig on available company resources or tech stacks, we could store that data anywhere and it can already be explored in the json format.
However, we can also extract it to csv, for more data science work. 
"""


#define folder variable
# json_folder = r'c:\Users\pc\Desktop\STELLA_SPACE\dpp_scrapy\web-scrapping'




# with open(data_source) as f:
#     data = json.load(f)

# # Open a CSV file to write to
# with open('Air_Now_Monitors_Ozone.csv', mode='w', newline='') as file:
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