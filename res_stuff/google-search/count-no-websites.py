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

counter = 0
for i,website in enumerate(res_info['website']):
    if i < 3000:
        if website == "No Website":
            counter += 1

print(counter)