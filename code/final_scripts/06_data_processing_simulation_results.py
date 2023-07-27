# Author: Bruno Marc J. Adam
# Last Update: 2023-07-03
# Purpose: Script to perform data processing on the simulation data and epw data

# University: DTU
# Master Thesis Project: Using AI to predict thermal comfort in buildings in South Africa

# Import libraries
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from toolbox.utils import import_simulation_data
from toolbox.epw  import import_epw


scenarios = ['present-day', '2050', '2080']
epw_files = [
    'ZAF_GT_Johannesburg.Botanical.Gardens.683610_TMYx.2004-2018.epw', 
    'ZAF_GT_Johannesburg.Botanical.Gardens.683610_TMYx.2004-2018_2050.epw', 
    'ZAF_GT_Johannesburg.Botanical.Gardens.683610_TMYx.2004-2018_2080.epw',
    ]

simulation_data = {}
for i, scenario in enumerate(scenarios):
    weather = import_epw(r'database/climate/' + epw_files[i])
    directory = r'simulations/' + scenario + '/outputs/'
    output_path = r'results/simulations/' + scenario + '_simulation_data.csv'
    simulation_data[scenario] = import_simulation_data(directory, weather, output_path)


