import pandas as pd
import numpy as np
import math
from math import sqrt
from geopy.distance import geodesic
import csv
import ast
import requests
from bs4 import BeautifulSoup
from googlesearch import search

res_info = pd.read_csv(r'C:\Save Data Here\Coding stuff\Projects\eatsee\eatsee_db\res_stuff\res_data\restaurant_info2.csv')

website_list = []
for i,original_website in enumerate(res_info['website']):
    if "wikipedia" in original_website:
        address = res_info['address'][i]
        try:
            website = next(search(address))
            website_list.append(website)
        except KeyboardInterrupt:
            print("keyboard interrupt: skip")
            website = original_website
            website_list.append(website)
    else:
        website_list.append(original_website)

res_info['website'] = website_list

res_info = res_info[['name', 'address', 'cuisine', 'lat', 'lon',
        'opening_hours', 'image_url', 'rating', 'coordinates', 'square_i',
        'square_j', 'nearest_town', 'website']].copy()

res_info.to_csv(r"C:\Save Data Here\Coding stuff\Projects\eatsee\eatsee_db\res_stuff\res_data\restaurant_info2.csv")

