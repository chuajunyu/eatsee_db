import pandas as pd
import numpy as np
import ast
import math
import os
from geopy.distance import geodesic

def create_restaurant_info_and_squares(print_dataframes=True, print_measurements=True, create_csv_files=True):
    # OBTAIN ORIGINAL DATA
    original_df = pd.read_csv(r'eatsee_db\res_stuff\res_data\Grab SG Restaurants.csv')
    restaurant_info = original_df[['name', 'address', 'cuisine', 'lat', 'lon', 'opening_hours', 'image_url', 'rating']].copy()

    if print_dataframes:
        print(restaurant_info.head(5))
        header = restaurant_info.columns.tolist()
        print(header, "\n")

    # MEASUREMENT INFO
    minLat = float('inf')
    maxLat = float('-inf')
    minLon = float('inf')
    maxLon = float('-inf')

    for i,n in enumerate(restaurant_info['name']):
        lat = restaurant_info['lat'][i]
        long = restaurant_info['lon'][i]

        minLat = float(min(minLat, lat))
        maxLat = float(max(maxLat, lat))
        minLon = float(min(minLon, long))
        maxLon = float(max(maxLon, long))

    # SG center (approx based on restaurants)
    sg_center_lat = (maxLat+minLat)/2
    sg_center_lon = (maxLon+minLon)/2
    sg_center = [sg_center_lat, sg_center_lon]
    # SG Lat and Lon distance/km (approx based on restaurants)
    sg_lat_dist = geodesic((minLat, sg_center[1]), (maxLat, sg_center[1])).kilometers
    sg_lon_dist = geodesic((sg_center[0], minLon), (sg_center[0], maxLon)).kilometers
    # SG Lat_unit and Lon_unit distance/km (approx based on restaurants)
    sg_lat_unit_dist = sg_lat_dist/9
    sg_lon_unit_dist = sg_lon_dist/14

    # square centers
    square_center_lat_list = []
    square_center_lon_list = []
    lat_unit = (maxLat-minLat)/9
    lon_unit = (maxLon-minLon)/14
    lat_center = minLat + lat_unit/2
    lon_center = minLon + lon_unit/2

    for index in range(9):
        square_center_lat_list.append(lat_center)
        lat_center += lat_unit

    for index in range(14):
        square_center_lon_list.append(lon_center)
        lon_center += lon_unit

    # SHOW ALL MEASURED INFO
    if print_measurements:
        print(f"minLat={minLat}, maxLat={maxLat}, minLon={minLon}, maxLon={maxLon}")
        print(f"sg_center = {sg_center}")
        print(f"lat_unit={lat_unit}, lon_unit={lon_unit} \n")
        print(f"sg_lat_unit_dist = {sg_lat_unit_dist}km, sg_lon_unit_dist = {sg_lon_unit_dist}km")
        print(f"sg_lat_dist = {sg_lat_dist}km, sg_lon_dist = {sg_lon_dist}km \n")
        print(f"square_center_lat_list = {square_center_lat_list}")
        print(f"square_center_lon_list = {square_center_lon_list} \n")

    # HELPER FUNCTIONS
    def find_square_i(lat_input, square_center_lat_list=square_center_lat_list):
        i_lat = min(square_center_lat_list, key=lambda x:abs(x-lat_input))
        return square_center_lat_list.index(i_lat)
    def find_square_j(lon_input, square_center_lon_list=square_center_lon_list):
        j_lon = min(square_center_lon_list, key=lambda x:abs(x-lon_input))
        return square_center_lon_list.index(j_lon)

    # HELPER INFO
    name_list = []
    coords_list = []
    square_i_list = []
    square_j_list = []
    cuisine_list = []
    num_list = []
    rating_list = []
    image_url_list = []
    open_hour_list = []
    nearest_town_list = []

    # MODIFY TOWN_INFO.CSV
    town_list = []
    town_dict = {}
    town_df = pd.read_csv(fr'eatsee_db\res_stuff\res_data\town_info.csv')
    # town_list = list(town_df['town'])
    for i,name in enumerate(town_df['town']):
        town_list.append(name)
        coordinates = ast.literal_eval(town_df['coordinates'][i])
        town_dict[name] = coordinates

    # MODIFY RES_INFO.CSV
    for i,name in enumerate(restaurant_info['name']):
        # NAMES
        address = restaurant_info['address'][i]
        if not isinstance(name, str):
            name = str(address.replace('Test', '').replace('TEST', '').replace('[', '').replace(']', ''))
        name_list.append(name)

        # ADDRESSES
        if not isinstance(address, str) or len(address)==0:
            address = "No address"

        # COORDINATES
        lat = restaurant_info['lat'][i]
        long = restaurant_info['lon'][i]
        coordinates = [lat, long]
        coords_list.append(coordinates)

        # I J SQUARES
        square_i = find_square_i(lat)
        square_j = find_square_j(long)
        square_i_list.append(square_i)
        square_j_list.append(square_j)

        # NEAREST TOWN
        nearest_town = min(town_list, key=lambda x:abs(geodesic(coordinates, town_dict[x]).kilometers))
        nearest_town_list.append(nearest_town)

        # CUISINES
        cuisines = restaurant_info['cuisine'][i]
        try:
            cuisines = cuisines.replace('"', '')
            cuisines = cuisines[1:-1].split(',')
            for index,cuisine in enumerate(cuisines):
                if cuisine[0] == ' ':
                    cuisines[index] = cuisine[1:]
            cuisine_list.append(cuisines)
        except AttributeError:
            cuisine_list.append(['None'])
            num_list.append(i)

        # IMAGE URLS
        image_url = restaurant_info['image_url'][i]
        if not isinstance(image_url, str):
            image_url = "No image_url"
        image_url_list.append(image_url)

        # RATINGS
        rating = restaurant_info['rating'][i]
        if math.isnan(rating):
            rating = 0
        rating_list.append(rating)

        # OPENING HOURS
        open_hours = restaurant_info['opening_hours'][i]
        open_hours = ast.literal_eval(open_hours.replace("true", "True").replace("false", "False"))
        open_hour_list.append(open_hours)

    restaurant_info['name'] = name_list
    restaurant_info['coordinates'] = coords_list
    restaurant_info['square_i'] = square_i_list
    restaurant_info['square_j'] = square_j_list
    restaurant_info['nearest_town'] = nearest_town_list
    restaurant_info['cuisine'] = cuisine_list
    restaurant_info['image_url'] = image_url_list
    restaurant_info['rating'] = rating_list
    restaurant_info['opening_hours'] = open_hour_list

    # SHOW END DATAFRAME
    if print_dataframes:
        print(restaurant_info)
        header = restaurant_info.columns.tolist()
        print(header)

    # WRITE TO CSV
    if create_csv_files:
        # restaurant_info.to_csv(r"path\to\output\csv\file")
        restaurant_info.to_csv(r"eatsee_db\res_stuff\res_data\restaurant_info.csv")

        # CREATE SQUARES
        try:
            os.makedirs(r"eatsee_db\res_stuff\res_data\squares")
        except FileExistsError:
            pass
        for square_i in range(9):
            for square_j in range(14):
                condition1 = restaurant_info['square_i'] == square_i
                condition2 = restaurant_info['square_j'] == square_j
                all_conditions = condition1 & condition2
                new_df = restaurant_info.loc[all_conditions]
                new_df.to_csv(fr"eatsee_db\res_stuff\res_data\squares\i{square_i}j{square_j}.csv", index=False, header=True)

        # CREATE TOWNS
        try:
            os.makedirs(r"eatsee_db\res_stuff\res_data\towns")
        except FileExistsError:
            pass
        for town in town_list:
            new_df = restaurant_info.loc[restaurant_info['nearest_town'] == town]
            town_name = town.replace(" ", "_")
            new_df.to_csv(fr"eatsee_db\res_stuff\res_data\towns\{town_name}.csv", index=False, header=True)


    # TESTING
    # for i,n in enumerate(restaurant_info['address']):
    #     if not isinstance(n, str) or not n:
    #         pass

create_restaurant_info_and_squares(print_dataframes=True, print_measurements=True, create_csv_files=True)