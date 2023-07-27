# Author: Bruno Marc J. Adam
# Last Update: 2023-07-03
# Purpose: Script to perform data processing on the inputs file of the simulations

# University: DTU
# Master Thesis Project: Using AI to predict thermal comfort in buildings in South Africa

# Import libraries
import pandas as pd
import numpy as np
import ast
from toolbox.utils import calculate_U_value
from datetime import datetime


# Import inputs file
scenarios = ['present-day', '2050', '2080']

inputs_dict = {}
for scenario in scenarios:
    path = 'simulations/' + scenario + '/inputs.csv'
    inputs_dict[scenario] = pd.read_csv(path)

# Clean Inputs data
for key in inputs_dict.keys():
    inputs_dict[key].rename(columns={'Unnamed: 0': 'key'}, inplace=True)
    inputs_dict[key]['volume'] = inputs_dict[key]['floor_area'] * inputs_dict[key]['building_height']

    inputs_dict[key]['floor_construction_list'] = inputs_dict[key]['floor_construction_list'].apply(ast.literal_eval)
    inputs_dict[key]['wall_construction_list'] = inputs_dict[key]['wall_construction_list'].apply(ast.literal_eval)
    inputs_dict[key]['roof_construction_list'] = inputs_dict[key]['roof_construction_list'].apply(ast.literal_eval)
    inputs_dict[key]['ground_construction_list'] = inputs_dict[key]['ground_construction_list'].apply(ast.literal_eval)
    
    inputs_dict[key]['floor_U_value'] = inputs_dict[key]['floor_construction_list'].apply(calculate_U_value)
    inputs_dict[key]['wall_U_value'] = inputs_dict[key]['wall_construction_list'].apply(calculate_U_value)
    inputs_dict[key]['roof_U_value'] = inputs_dict[key]['roof_construction_list'].apply(calculate_U_value)
    inputs_dict[key]['ground_U_value'] = inputs_dict[key]['ground_construction_list'].apply(calculate_U_value)

    inputs_dict[key]['door_area'] = inputs_dict[key]['door_width']* inputs_dict[key]['door_height_fraction_building_height'] * inputs_dict[key]['building_height']
    
    inputs_dict[key]['wall_construction'] = inputs_dict[key]['wall_construction_list'].apply(lambda x: 1 if 'Concrete' in str(x) else 0)
    inputs_dict[key]['roof_construction'] = inputs_dict[key]['roof_construction_list'].apply(lambda x: 1 if 'Concrete' in str(x) else 0)
    inputs_dict[key]['ground_construction'] = inputs_dict[key]['ground_construction_list'].apply(lambda x: 1 if 'Concrete' in str(x) else 0)
    inputs_dict[key]['floor_construction'] = inputs_dict[key]['floor_construction_list'].apply(lambda x: 1 if 'Concrete' in str(x) else 0)

    inputs_dict[key]['construction_type'] = inputs_dict[key][['wall_construction', 'roof_construction', 'ground_construction']].mode(axis=1)[0]
    
    inputs_dict[key]['ceiling_insulation'] = inputs_dict[key]['roof_construction_list'].apply(lambda x: 1 if 'Insulation' in str(x) else 0)

    inputs_dict[key] = inputs_dict[key][['key', 'floor_area', 'volume', 'orientation', 'wall_U_value', 'roof_U_value', 'ground_U_value', 'construction_type', 'ceiling_insulation', 'u_factor', 'shgc', 'window_to_wall_ratio', 'door_area', 'number_people', 'activity_level', 'P_equip', 'elec_gas','P_hvac', 'lighting_bulbs', 'infiltration_rate', 'type_house']]
    
    inputs_dict[key].set_index('key', inplace=True)

    print('\n\n Scenario: ' + key)
    print(inputs_dict[key].info())


# Import failed simulations
failed_index = {}
for scenario in scenarios:
    path = 'simulations/' + scenario + '/failed_simulations.csv'
    failed_simulations = pd.read_csv(path)
    failed_simulations = failed_simulations.T
    failed_index[scenario] = failed_simulations.index[1:].values.astype(int)
    


# Exclude failed simulations
for key in inputs_dict.keys():
    inputs_dict[key] = inputs_dict[key].drop(failed_index[key])
    print('\n\n Scenario: ' + key)
    print(inputs_dict[key].info())


inputs_dict['present-day'].head()


# Save inputs
for key in inputs_dict.keys():
    path = 'results/simulations/' + key + '_inputs.csv'
    inputs_dict[key].to_csv(path)


