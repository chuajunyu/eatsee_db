import pandas as pd
import numpy as np
import math
from math import sqrt
from geopy.distance import geodesic

location_res = pd.read_csv(r'SQL\location_res.csv')
myCoords = myCoords = [1.3, 103.7]

distance=[]
for i,n in enumerate(location_res['name']):
    lat = location_res['lat'][i]
    long = location_res['lon'][i]

    point1 = (lat, long)
    point2 = (myCoords[0], myCoords[1])

    dist = geodesic(point1, point2).kilometers

    distance.append(dist)

location_res['distance'] = distance
final_df = location_res.loc[location_res['distance'] <= 4]
print(final_df)