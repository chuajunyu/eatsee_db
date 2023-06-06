import pandas as pd
import numpy as np
import math
import ast
from math import sqrt
from geopy.distance import geodesic

def find_square_i(lat_input, square_center_lat_list=[1.2437071777777777, 1.2702135333333333, 1.296719888888889, 1.3232262444444445, 1.3497326, 1.3762389555555556, 1.4027453111111112, 1.4292516666666668, 1.4557580222222224]):
    i_lat = min(square_center_lat_list, key=lambda x:abs(x-lat_input))
    return square_center_lat_list.index(i_lat)
def find_square_j(lon_input, square_center_lon_list=[103.63894748571428, 103.66548865714286, 103.69202982857144, 103.71857100000001, 103.74511217142859, 103.77165334285716, 103.79819451428574, 103.82473568571432, 103.85127685714289, 103.87781802857147, 103.90435920000004, 103.93090037142862, 103.9574415428572, 103.98398271428577]):
    j_lon = min(square_center_lon_list, key=lambda x:abs(x-lon_input))
    return square_center_lon_list.index(j_lon)

def find_closest_string_lev(string_list, string_a):

    def levenshtein_distance(string1, string2):
        if len(string1) < len(string2):
            return levenshtein_distance(string2, string1)

        if len(string2) == 0:
            return len(string1)

        previous_row = range(len(string2) + 1)

        for i, char1 in enumerate(string1):
            current_row = [i + 1]

            for j, char2 in enumerate(string2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (char1 != char2)
                current_row.append(min(insertions, deletions, substitutions))

            previous_row = current_row

        return previous_row[-1]
    
    closest_string = None
    closest_distance = float('inf')  # Initialize with a large value

    for string in string_list:
        distance = levenshtein_distance(string, string_a)  # Calculate the Levenshtein distance
        if distance < closest_distance:
            closest_distance = distance
            closest_string = string

    return closest_string

def find_closest_string_jaccard(string_list, string_a):

    def jaccard_similarity(string1, string2):
        set1 = set(string1.lower())
        set2 = set(string2.lower())
        intersection = len(set1.intersection(set2))
        union = len(set1) + len(set2) - intersection
        return intersection / union if union != 0 else 0
    
    closest_string = None
    highest_similarity = 0.0

    for string in string_list:
        similarity = jaccard_similarity(string, string_a)  # Calculate the Jaccard similarity
        if similarity > highest_similarity:
            highest_similarity = similarity
            closest_string = string

    return closest_string

def find_res_optim(user_coords: list =[], town: str ="tampines", max_distance: float =2, cuisine_whitelist: list =[], diet_whitelist: list =[], cuisine_diet_blacklist: list =[], include_all_cuisines: bool =True):
    # if got Town
    town = town.upper()
    if (len(town) == 0) or (town == "NONE"):
        town = False
    else:
        town_info = pd.read_csv(r'res_stuff\res_data\town_info.csv')
        town_list = list(town_info["town"])
        if town not in town_list:
            town = find_closest_string_jaccard(town_list, town)

    # if got Coords
    if user_coords:
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
                    df_list.append(pd.read_csv(fr'res_stuff\res_data\squares\i{i}j{j}.csv'))
                except FileNotFoundError:
                    pass
        
        try:
            combined_df = pd.concat(df_list, ignore_index=True)
        except ValueError:
            return False
        
        if town:
            combined_df = combined_df.loc[combined_df['nearest_town'] == town]
        
        try:
            actual_distances=[]
            for i in range(len(combined_df)):
                lat = combined_df['lat'][i]
                long = combined_df['lon'][i]

                point1 = (lat, long)
                point2 = (user_coords[0], user_coords[1])

                dist = geodesic(point1, point2).kilometers

                actual_distances.append(dist)
        except KeyError:
            return False

        combined_df['distance'] = actual_distances
        # filter max_distance
        final_df = combined_df.loc[combined_df['distance'] < max_distance]
    
    else:
        if town:
            town_name = town.replace(" ", "_")
            final_df = pd.read_csv(fr'res_stuff\res_data\towns\{town_name}.csv')

        else:
            return False


    # filter cuisinine whitelist
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

    final_dict = final_df.to_dict(orient='records')

    return final_dict