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

def find_res_optim(user_coords: list =[1.3497325999999998, 103.81146509999999], max_distance: float =2, cuisine_whitelist: list =[], diet_whitelist: list =[], cuisine_diet_blacklist: list =[], include_all_cuisines: bool =True):
    
    user_i = find_square_i(user_coords[0])
    user_j = find_square_j(user_coords[1])
    SQUARE_RANGE = math.ceil(max_distance/2.9309374423747543)

    i_min = user_i - SQUARE_RANGE
    i_max = user_i + SQUARE_RANGE
    j_min = user_j - SQUARE_RANGE
    j_max = user_j + SQUARE_RANGE
    df_list = []

    for i in range(i_min, i_max+1):
        for j in range(j_min, j_max+1):
            try:
                df_list.append(pd.read_csv(fr'C:\Save Data Here\Coding stuff\Projects\eatsee\eatsee_db\res_stuff\res_data\squares\i{i}j{j}.csv'))
            except FileNotFoundError:
                pass
    
    try:
        combined_df = pd.concat(df_list, ignore_index=True)
    except ValueError:
        return ('No restaurants found')

    actual_distances=[]
    for i in range(len(combined_df)):
        lat = combined_df['lat'][i]
        long = combined_df['lon'][i]

        point1 = (lat, long)
        point2 = (user_coords[0], user_coords[1])

        dist = geodesic(point1, point2).kilometers

        actual_distances.append(dist)

    combined_df['distance'] = actual_distances
    # filter max_distance
    final_df = combined_df.loc[combined_df['distance'] <= max_distance]
    # filter cuisinine whitelist
    def to_lower(string1):
        return string1.lower()
    if cuisine_whitelist:
        if include_all_cuisines:
            final_df = final_df.loc[final_df['cuisine'].apply(lambda x: all(cuisine.lower() in x.lower() for cuisine in cuisine_whitelist))]
        else:
            final_df = final_df.loc[final_df['cuisine'].str.contains('|'.join(cuisine_whitelist), case=False)]
    # filter diet whielist
    if diet_whitelist:
        final_df = final_df.loc[final_df['cuisine'].apply(lambda x: all(cuisine.lower() in x.lower() for cuisine in diet_whitelist))]
    # filter blacklist
    if cuisine_diet_blacklist:
        black_diets = ~final_df['cuisine'].str.contains('|'.join(cuisine_diet_blacklist))
        final_df = final_df.loc[black_diets]


    print(final_df)
    header = final_df.columns.tolist()
    print(header)
    final_dict = final_df.to_dict(orient='records')

    return final_dict

# find_res_optim()