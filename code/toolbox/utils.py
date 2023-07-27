import pandas as pd
import numpy as np 
# Ignore warnings
import warnings
warnings.filterwarnings("ignore")
from IPython.display import clear_output
import os
import time
from datetime import timedelta

def nan_counter(list_of_series):
    nan_polluted_series_counter = 0
    for series in list_of_series:
        if series.isnull().sum().sum() > 0:
            nan_polluted_series_counter+=1
    print(nan_polluted_series_counter)

# Create definition to import data from csv files in a table format with date as index and time as columns to a timeseries format
def import_saws_data(filename):
    df = pd.read_csv(filename, sep=',')
    ts = pd.Series()
    m, n = df.shape
    for i in range(0, m):
        for j in range(1, n):
            try:
                date = df.iloc[i, 0]
                time = str.replace(df.columns[j], '.', ':')
                # Convert date DD/MM/YYYY to datetime
                date = pd.to_datetime(date, format='%d/%m/%Y')
                if time == '00:00':
                    # Add one day to date
                    date = date + pd.DateOffset(days=1)
                datetime = pd.to_datetime(str(date.date())+ ' ' + time)
                ts[datetime] = df.iloc[i, j]
            except: 
                pass
    return ts

def calculate_U_value(list):
    resistance = []
    for i in list:
        thickness = i[1]
        conductivity = i[2]
        resistance.append(thickness/conductivity)
    return 1/sum(resistance)

def import_simulation_data(directory_path, weather, output_path):
    scenario = directory_path.split('/')[2]

    folders = os.listdir(directory_path)

    simulation_data = {}
    # Start the timer
    start = time.time()
    for i, key in enumerate(folders):
        clear_output(wait=True)
        file = directory_path + key + '/eplusout.csv'
        simulation_data[key] = pd.read_csv(file)

        # Convert the date and time to datetime format
        simulation_data[key]['Date/Time'] = simulation_data[key]['Date/Time'].astype(str)
        simulation_data[key]['Date/Time'] = '2023/' + simulation_data[key]['Date/Time']
        simulation_data[key]['Date/Time'] = simulation_data[key]['Date/Time'].str.replace('2023/ ', '2023/')
        simulation_data[key]['Date/Time'] = simulation_data[key]['Date/Time'].str.replace('24:00:00', '00:00:00')
        simulation_data[key]['Date/Time'] = pd.to_datetime(simulation_data[key]['Date/Time'], format='%Y/%m/%d  %H:%M:%S')
        for i in range(len(simulation_data[key]['Date/Time'])):
            if simulation_data[key]['Date/Time'][i].hour == 0 and simulation_data[key]['Date/Time'][i].minute == 0 and simulation_data[key]['Date/Time'][i].second == 0:
                simulation_data[key]['Date/Time'][i] = simulation_data[key]['Date/Time'][i] + timedelta(days=1)
    
        # Resample the data to hourly
        simulation_data[key] = simulation_data[key].set_index('Date/Time').resample('1H').mean().reset_index()
        
        # Keep the columns of interest and rename them
        simulation_data[key] = simulation_data[key][[
            'Date/Time', 
            'THERMAL ZONE:Zone Mean Air Temperature [C](TimeStep)', 
            'THERMAL ZONE:Zone Air Relative Humidity [%](TimeStep)']]
        
        simulation_data[key] = pd.merge(simulation_data[key], weather, how='left', left_on='Date/Time', right_on='datetime')

        simulation_data[key] = simulation_data[key].rename(columns={
            'Date/Time': 'Datetime',
            'THERMAL ZONE:Zone Mean Air Temperature [C](TimeStep)': 'Indoor Mean Air Temperature',
            'THERMAL ZONE:Zone Air Relative Humidity [%](TimeStep)': 'Indoor Air Relative Humidity'})
        
        # Set the index to datetime
        simulation_data[key] = simulation_data[key].set_index('Datetime')
        simulation_data[key]['key'] = key

        if folders.index(key) % 10 == 0:
            print('{} - Progress: {}/{} - {} seconds'.format(scenario, folders.index(key), len(folders), round(time.time() - start, 2)))

    # Concatenate all the dataframes
    df = pd.concat(simulation_data)

    clear_output(wait=True)
    print('Done in {} minutes'.format(round((time.time() - start)/60, 2)))
    print('Saving the data...')
    df.to_csv(output_path)
    print('Data saved in {}!'.format(output_path))
    return df