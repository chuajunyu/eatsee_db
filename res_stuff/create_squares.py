import pandas as pd
import numpy as np
import math
from math import sqrt
from geopy.distance import geodesic

location_res = pd.read_csv(r'eatsee_db\res_stuff\res_data\location_res.csv')
columns = ["name", "address", "cuisine", "lat", "lon", "image_url", "rating", "coordinates", "square_i", "square_j"]

for square_i in range(9):
    for square_j in range(14):
        condition1 = location_res['square_i'] == square_i
        condition2 = location_res['square_j'] == square_j
        mask = condition1 & condition2
        new_df = location_res.loc[mask]
        new_df.columns = new_df.columns.str.lstrip(',')
        new_df.to_csv(fr"eatsee_db\res_stuff\res_data\squares\i{square_i}j{square_j}.csv", index=False, header=True)