import pandas as pd
import numpy as np
import math
from math import sqrt
from geopy.distance import geodesic

def find_square_i(lat_input, square_center_lat_list=[1.2437071777777777, 1.2702135333333333, 1.296719888888889, 1.3232262444444445, 1.3497326, 1.3762389555555556, 1.4027453111111112, 1.4292516666666668, 1.4557580222222224]):
    i_lat = min(square_center_lat_list, key=lambda x:abs(x-lat_input))
    return square_center_lat_list.index(i_lat)
def find_square_j(lon_input, square_center_lon_list=[103.63894748571428, 103.66548865714286, 103.69202982857144, 103.71857100000001, 103.74511217142859, 103.77165334285716, 103.79819451428574, 103.82473568571432, 103.85127685714289, 103.87781802857147, 103.90435920000004, 103.93090037142862, 103.9574415428572, 103.98398271428577]):
    j_lon = min(square_center_lon_list, key=lambda x:abs(x-lon_input))
    return square_center_lon_list.index(j_lon)

myCoords = myCoords = [1.3, 103.7]

user_i = find_square_i(myCoords[0])
user_j = find_square_j(myCoords[1])

i_min = user_i - 1
i_max = user_i + 1
j_min = user_j - 1
j_max = user_j + 1
df_list = []

for i in range(i_min, i_max+1):
    for j in range(j_min, j_max+1):
        df_list.append(pd.read_csv(fr'SQL\squares\i{i}j{j}.csv'))

combined_df = pd.concat(df_list, ignore_index=True)

distance=[]
for i,n in enumerate(combined_df['name']):
    lat = combined_df['lat'][i]
    long = combined_df['lon'][i]

    point1 = (lat, long)
    point2 = (myCoords[0], myCoords[1])

    dist = geodesic(point1, point2).kilometers

    distance.append(dist)

combined_df['distance'] = distance
final_df = combined_df.loc[combined_df['distance'] <= 2]
print(final_df)
print(final_df.to_dict(orient='records'))
