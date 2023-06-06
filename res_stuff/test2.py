import pandas as pd
import numpy as np
import math
from math import sqrt
from geopy.distance import geodesic
import csv
import ast

res_info = pd.read_csv(R'eatsee_db\res_stuff\res_data\restaurant_info.csv')
town_info = pd.read_csv(R'eatsee_db\res_stuff\res_data\town_info.csv')
town_list = list(town_info['town'])

town_dict = {}
counter = 0

string1 = 'a'

if string1:
    print('hello')
