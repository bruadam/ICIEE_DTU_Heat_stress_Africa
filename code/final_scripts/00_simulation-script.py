# This script is used to run the simulation and generate the results for a given set of parameters and N sets of inputs for the simulation. N is the number of parametric runs.

# Last updated: 2023-06-24

#%% LIBRARIES
import pandas as pd
import numpy as np
import sys
import time
from IPython.display import clear_output

from pyosmodel import utils
from pyosmodel.model import simulate_model
from pyosmodel.predefinedmodel import define_RDP_inputs, define_shack_inputs
from pyosmodel.params import change_timestep
from pyosmodel.simulation import run_simulation

#%% SETTINGS
# Number of simulations to run
Number_simulations = 500 # Must be even
N = int(Number_simulations/2)

# Definition of the inputs for the simulation
inputs = pd.DataFrame()
inputs = define_RDP_inputs(N)
inputs = pd.concat([inputs, define_shack_inputs(N)], 
                   ignore_index=True)

# Definition of required directories
eplus_install_dir=r'C:/EnergyPlusV23-1-0'

# Setting up the output parameters
output_data = ['Zone Air Relative Humidity',
               'Zone Mean Air Temperature',
               'Zone Mean Radiant Temperature',
               'People Occupant Count',
               'Lights Total Heating Rate',
               'Electric Equipment Total Heating Rate',
               'Zone Windows Total Heat Loss Rate',
               'Zone Windows Total Heat Gain Rate',
               'Infiltration Air Change Rate',
               'Zone Infiltration Air Change Rate',
               'Zone Thermostat Heating Setpoint Temperature']

# Setting up the simulation timestep
step = 4 # one value every 15 minutes

output_directory_paths = ['simulations/present-day/',
                            'simulations/2050/',
                            'simulations/2080/']

epw_paths = [r'database/climate/ZAF_GT_Johannesburg.Botanical.Gardens.683610_TMYx.2004-2018.epw',
            r'database/climate/ZAF_GT_Johannesburg.Botanical.Gardens.683610_TMYx.2004-2018_2050.epw',
            r'database/climate/ZAF_GT_Johannesburg.Botanical.Gardens.683610_TMYx.2004-2018_2080.epw']

for output_directory_path, epw_path in zip(output_directory_paths, epw_paths):
    # Save the inputs in a csv file
    inputs.to_csv(output_directory_path + 'inputs.csv')
    # Setting up the output directory
    utils.output_directory(output_directory_path)

    # Storing the failed simulations inputs in a csv file for exploration
    failed_simulations = pd.DataFrame()

    #%% SIMULATION
    print('Starting simulation')
    start = time.time()

    # Simulation Core
    for i in range(Number_simulations):
        try:
            # Define the model
            item_inputs = inputs.loc(axis=0)[i]
            model = simulate_model(item_inputs, output_data, epw_path)
            change_timestep(model, step)
            
            # Save the model in an idf file
            output_directory = output_directory_path + 'outputs/' + str(i) + '/'
            idf_path = output_directory_path + 'models/' + str(i) + '.idf'
            utils.save_model_to_idf(model, idf_path)

            # Run the simulation
            result = run_simulation(idf_path, epw_path, output_directory, eplus_install_dir)

        except:
            # Concatenate the failed simulations
            failed_simulations = pd.concat([failed_simulations, item_inputs], axis=1)
            continue
        utils.clear_screen()
        # For every 10 simulations, print the progress
        if i % 10 == 0:
            duration = time.time() - start
            estimated_time_left = duration/(i+1)*(Number_simulations-i-1)/60
            # 
            print('Progression ' + str(i) + '/' + str(Number_simulations) + ' Estimated time left:' + str(estimated_time_left) + '\n\n\n')

    utils.clear_screen()
    # Save the failed simulations in a csv file
    failed_simulations.to_csv(output_directory_path + 'failed_simulations.csv')

    end = time.time()
    print('Total time: ' + str(end - start))
    print('{} Simulations failed'.format(failed_simulations.shape[1]))
    print('Finished one set of simulations')

print('Finished')


