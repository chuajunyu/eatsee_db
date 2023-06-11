import pandas as pd
import numpy as np
import ast
import math
import os
from geopy.distance import geodesic

def create_restaurant_info_and_squares(print_dataframes=True, print_measurements=True, create_csv_files=True):
    # WRITE TO CSV
    town_list = []
    town_df = pd.read_csv(r'res_data\town_info.csv')
    for i,name in enumerate(town_df['town']):
        town_list.append(name)

    if create_csv_files:
        # restaurant_info.to_csv(r"path\to\output\csv\file")
        restaurant_info = pd.read_csv(r'res_data\restaurant_info_final.csv')

        # CREATE SQUARES
        try:
            os.makedirs(r"res_data\squares")
        except FileExistsError:
            pass
        for square_i in range(9):
            for square_j in range(14):
                condition1 = restaurant_info['square_i'] == square_i
                condition2 = restaurant_info['square_j'] == square_j
                all_conditions = condition1 & condition2
                new_df = restaurant_info.loc[all_conditions]
                new_df.to_csv(fr"res_data\squares\i{square_i}j{square_j}.csv", index=False, header=True)

        # CREATE TOWNS
        try:
            os.makedirs(r"res_data\towns")
        except FileExistsError:
            pass
        for town in town_list:
            new_df = restaurant_info.loc[restaurant_info['nearest_town'] == town]
            town_name = town.replace(" ", "_")
            new_df.to_csv(fr"res_data\towns\{town_name}.csv", index=False, header=True)


    # TESTING
    # for i,n in enumerate(restaurant_info['address']):
    #     if not isinstance(n, str) or not n:
    #         pass

create_restaurant_info_and_squares(print_dataframes=True, print_measurements=True, create_csv_files=True)