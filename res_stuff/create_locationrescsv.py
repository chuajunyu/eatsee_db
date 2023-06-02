import pandas as pd
import numpy as np
import math
from math import sqrt
from geopy.distance import geodesic

original_df = pd.read_csv(r'SQL\Grab SG Restaurants.csv')
location_res = original_df[['name', 'address', 'cuisine', 'lat', 'lon', 'image_url', 'rating']].copy()

coords = []
for i,n in enumerate(location_res['name']):
    a = [location_res['lat'][i],location_res['lon'][i]]
    coords.append(a)
location_res['coordinates'] = coords

print(location_res.head(5))
header = location_res.columns.tolist()
print(header, "\n")

minLat = float('inf')
maxLat = float('-inf')
minLon = float('inf')
maxLon = float('-inf')

for i,n in enumerate(location_res['name']):
    lat = location_res['lat'][i]
    long = location_res['lon'][i]

    minLat = float(min(minLat, lat))
    maxLat = float(max(maxLat, lat))
    minLon = float(min(minLon, long))
    maxLon = float(max(maxLon, long))

print(f"minLat={minLat}, maxLat={maxLat}, minLon={minLon}, maxLon={maxLon}")

lat_unit = (maxLat-minLat)/9
lon_unit = (maxLon-minLon)/14

print(f"lat_unit={lat_unit}, lon_unit={lon_unit} \n")

sg_center_lat = (maxLat+minLat)/2
sg_center_lon = (maxLon+minLon)/2
sg_center = [sg_center_lat, sg_center_lon]

print(f"sg_center = {sg_center}")

sg_lat_dist = geodesic((minLat, sg_center[1]), (maxLat, sg_center[1])).kilometers
sg_lon_dist = geodesic((sg_center[0], minLon), (sg_center[0], maxLon)).kilometers

print(f"sg_lat_dist = {sg_lat_dist}km, sg_lon_dist = {sg_lon_dist}km \n")

# SQUARE CENTER

square_center_lat_dict = {}
square_center_lon_dict = {}
square_center_lat_list = []
square_center_lon_list = []

lat_center = minLat + lat_unit/2
lon_center = minLon + lon_unit/2

for index in range(9):
    square_center_lat_list.append(lat_center)
    lat_center += lat_unit

for index in range(14):
    square_center_lon_list.append(lon_center)
    lon_center += lon_unit


print(f"square_center_lat_list = {square_center_lat_list}")
print(f"square_center_lon_list = {square_center_lon_list} \n")


def find_square_i(lat_input, square_center_lat_list=square_center_lat_list):
    i_lat = min(square_center_lat_list, key=lambda x:abs(x-lat_input))
    return square_center_lat_list.index(i_lat)
def find_square_j(lon_input, square_center_lon_list=square_center_lon_list):
    j_lon = min(square_center_lon_list, key=lambda x:abs(x-lon_input))
    return square_center_lon_list.index(j_lon)

square_i_list = []
square_j_list = []
for i,n in enumerate(location_res['name']):
    lat = location_res['lat'][i]
    long = location_res['lon'][i]
    square_i = find_square_i(lat)
    square_j = find_square_j(long)
    square_i_list.append(square_i)
    square_j_list.append(square_j)

location_res['square_i'] = square_i_list
location_res['square_j'] = square_j_list

print(location_res)
header = location_res.columns.tolist()
print(header)

# location_res.to_csv(r"path\to\output\csv\file")