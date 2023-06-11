import pandas as pd
import numpy as np
import math
from math import sqrt
from geopy.distance import geodesic
import csv
import ast
from googlesearch import search
import csv
import requests
from bs4 import BeautifulSoup

def main():
    res_info = pd.read_csv(r"C:\Save Data Here\Coding stuff\Projects\eatsee\eatsee_db\res_stuff\res_data\restaurant_info2.csv")
    counter = 0

    website_dict={}
    for i,name in enumerate(res_info['name']):
        website = res_info['website'][i]
        if website != "No Website":
            website_dict[name] = website
        else: counter+=1

    print(counter)
        
    # print(website_dict)
    # print(len(website_dict))

    website_list=[]
    for i,name in enumerate(res_info['name']):
        website = website_dict.get(name, "No Website")
        website_list.append(website)

    res_info['website'] = website_list

    res_info = res_info[['name', 'address', 'cuisine', 'lat', 'lon',
        'opening_hours', 'image_url', 'rating', 'coordinates', 'square_i',
        'square_j', 'nearest_town', 'website']].copy()

    res_info.to_csv(r"C:\Save Data Here\Coding stuff\Projects\eatsee\eatsee_db\res_stuff\res_data\restaurant_info2.csv")

for i in range(3):
    main()
