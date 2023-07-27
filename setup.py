# Author: Bruno Marc J. Adam
# Last Update: 2023-07-03
# Purpose: Script to run all the project scripts in the correct order and create the necessary directories

# University: DTU
# Master Thesis Project: Using AI to predict thermal comfort in buildings in South Africa

# Import libraries
import os
import sys

sys.path.append('C://thesis/code/toolbox')
sys.path.append('C://thesis/code/pyosmodel')

# Run command to install the libraries in requirements.txt
# os.system('python -m pip install -r requirements.txt')

if not os.path.exists('database'):
    # Create the necessary directories
    os.system('mkdir database')
# Create a folder /database/cleaned if it does not exist
if not os.path.exists('database/cleaned'):
    os.makedirs('database/cleaned')
if not os.path.exists('database/cleaned/johannesburg'):
    os.makedirs('database/cleaned/johannesburg')
if not os.path.exists('database/cleaned/giyani'):
    os.makedirs('database/cleaned/giyani')
if not os.path.exists('simulations'):
    os.makedirs('simulations')
if not os .path.exists('simulations/2050'):
    os.makedirs('simulations/2050')
if not os.path.exists('simulations/2080'):
    os.makedirs('simulations/2080')
if not os.path.exists('simulations/present-day'):
    os.makedirs('simulations/present-day')
if not os.path.exists('simulations/2050/models'):
    os.makedirs('simulations/2050/models')
if not os.path.exists('simulations/2080/models'):
    os.makedirs('simulations/2080/models')
if not os.path.exists('simulations/present-day/models'):
    os.makedirs('simulations/present-day/models')
if not os.path.exists('simulations/2050/outputs'):
    os.makedirs('simulations/2050/outputs')
if not os.path.exists('simulations/2080/outputs'):
    os.makedirs('simulations/2080/outputs')
if not os.path.exists('simulations/present-day/outputs'):
    os.makedirs('simulations/present-day/outputs')
if not os.path.exists('results'):
    os.makedirs('results')
if not os.path.exists('results/features'):
    os.makedirs('results/features')
if not os.path.exists('results/models'):
    os.makedirs('results/models')
if not os.path.exists('results/simulations'):
    os.makedirs('results/simulations')
if not os.path.exists('results/ts_clustering'):
    os.makedirs('results/ts_clustering')

if os.path.exists('simulations'):
    # Check if the size of the folder /simulations is greater than 0
    if os.path.getsize('simulations') > 0:
        simulation_toggle = False
    else:
        simulation_toggle = True

if simulation_toggle:
    os.system('python code/final_scripts/00_simulation-script.py')

# Run the data processing scripts
os.system('python code/final_scripts/01_data_processing_weather_johannesburg.py')
os.system('python code/final_scripts/02_data_processing_weather_giyani.py')
os.system('python code/final_scripts/04_data_processing_giyani.py')
os.system('python code/final_scripts/03_data_processing_johannesburg.py')
simulation_processing = input('Do you want to process the simulation results? (y/n) ')
if simulation_processing == 'y':
    os.system('python code/final_scripts/05_data_processing_simulation_inputs.py')
    os.system('python code/final_scripts/06_data_processing_simulation_results.py')

features = input('Do you want to run the features engineering scripts? (y/n) ')
if features == 'y':
    os.system('python code/final_scripts/07_data_augmentation.py')
    os.system('python code/final_scripts/08_features_selection.py')
    os.system('python code/final_scripts/09_features_minimum_required.py')

models = input('Do you want to run the machine learning part? (y/n) ')
if models == 'y':
    os.system('python code/final_scripts/10_ml_models_best_performing.py')
    os.system('python code/final_scripts/11_ml_models_fine_tuning.py')

sensitivity = input('Do you want to run the sensitivity analysis? (y/n) ')
if sensitivity == 'y':
    os.system('python code/final_scripts/12_sensitivity_analysis.py')

figures = input('Do you want to run the figures scripts? (y/n) ')
if figures == 'y':
    os.system('python code/final_scripts/figures.py')

print('All the scripts have been run successfully!')