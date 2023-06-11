import pandas as pd
import numpy as np
import math
from math import sqrt
from geopy.distance import geodesic
import csv
import ast
from googlesearch import search
import time

def add_websites(): # add websites to restaurants if certain conditions met
    res_info = pd.read_csv(r"C:\Save Data Here\Coding stuff\Projects\eatsee\eatsee_db\res_stuff\res_data\restaurant_info2.csv")

    website_list = []
    for i,name in enumerate(res_info['address']): # use res_info['name'] or res_info['address'] as search query
        original_website = res_info['website'][i]
        if (i>=0) and ("google" in original_website): # conditions for searching restaurant's website
            print(i)
            print(name)
            try:
                website = next(search(name))
            except KeyboardInterrupt: # Ctrl-C terminal to skip current restaurant's search
                print("keyboard interrupt: skip")
                website = original_website
            except Exception as e:
                website = original_website
                print(e)
            website_list.append(website)
            print(website)
        else:
            website_list.append(original_website)

    res_info['website'] = website_list

    res_info = res_info[['name', 'address', 'cuisine', 'lat', 'lon',
        'opening_hours', 'image_url', 'rating', 'coordinates', 'square_i',
        'square_j', 'nearest_town', 'website']].copy()

    res_info.to_csv(r"C:\Save Data Here\Coding stuff\Projects\eatsee\eatsee_db\res_stuff\res_data\restaurant_info2.csv")

def copy_websites(): # copy-paste restaurant websites to restaurants with same names
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


add_websites()
for i in range(3):
    copy_websites()
