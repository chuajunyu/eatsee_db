import pandas as pd
import numpy as np
import math
from math import sqrt
from geopy.distance import geodesic
import csv
import ast
from googlesearch import search
import time

res_info = pd.read_csv(r"C:\Save Data Here\Coding stuff\Projects\eatsee\eatsee_db\res_stuff\res_data\restaurant_info2.csv")

website_list = []
for i, name in enumerate(res_info['name']):
    original_website = res_info['website'][i]
    while True:
        if (i > 1237) and (original_website == "No Website"):
            print(name)
            start_time = time.time()
            try:
                for website in search(name):
                    elapsed_time = time.time() - start_time
                    if elapsed_time >= 10:
                        break
                    website_list.append(website)
                    print(website)
                    break
            except Exception as e:
                website = original_website
                print(e)
                website_list.append(website)
        else:
            website_list.append(original_website)

res_info['website'] = website_list

res_info = res_info[['name', 'address', 'cuisine', 'lat', 'lon',
                     'opening_hours', 'image_url', 'rating', 'coordinates', 'square_i',
                     'square_j', 'nearest_town', 'website']].copy()

res_info.to_csv(r"C:\Save Data Here\Coding stuff\Projects\eatsee\eatsee_db\res_stuff\res_data\restaurant_info2.csv", index=False)
