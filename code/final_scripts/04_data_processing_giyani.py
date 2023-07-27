# Author: Bruno Marc J. Adam
# Last Update: 2023-07-03
# Purpose: Script to perform Data Processing on the data from Giyani, South Africa

# University: DTU
# Master Thesis Project: Using AI to predict thermal comfort in buildings in South Africa

# Import libraries
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import os


path_directory_winter = 'database/giyani/winter/'
path_directory_summer = 'database/giyani/others/'

paths_winter = os.listdir(path_directory_winter)
for path in paths_winter:
    if os.path.getsize(path_directory_winter + path) < 5000:
        paths_winter.remove(path)

paths_summer = os.listdir(path_directory_summer)
for path in paths_summer:
    if os.path.getsize(path_directory_summer + path) < 5000:
        paths_summer.remove(path)


# Import WINTER data

df_winter = {}
for path in paths_winter:
    df_winter[path] = pd.read_csv(path_directory_winter + path, header = None)

    df_winter[path] = df_winter[path].drop([2, 4], axis = 1)
    df_winter[path].columns = ['Datetime', 'Indoor Mean Air Temperature', 'Indoor Air Relative Humidity']
    df_winter[path]['Datetime'] = pd.to_datetime(df_winter[path]['Datetime'])

    df_winter[path] = df_winter[path].loc[(df_winter[path]['Indoor Air Relative Humidity'] >= 0) & (df_winter[path]['Indoor Air Relative Humidity'] <= 100)]
    df_winter[path]['key'] = path[:-4] 
    df_winter[path]['Season'] = 'Winter'
    
df_winter = pd.concat(df_winter, ignore_index=True)

# Clean data

df_winter['Indoor Mean Air Temperature'] = df_winter['Indoor Mean Air Temperature'].apply(lambda x: float(x) if isinstance(x, float) else np.nan)
df_winter['Indoor Air Relative Humidity'] = df_winter['Indoor Air Relative Humidity'].apply(lambda x: float(x) if isinstance(x, float) else np.nan)

print('Info about the data set:')
print(df_winter.info())


# Clean WINTER data
strings = df_winter[~df_winter['Indoor Mean Air Temperature'].astype(str).str.contains(r'^-?\d+\.?\d*$')]['Indoor Mean Air Temperature'].unique()
print('Non-numeric values in the data set : {} \n'.format(strings))

df_winter.replace('> 85.0 ', np.nan, inplace=True)

# Convert to numeric
df_winter['Indoor Mean Air Temperature'] = pd.to_numeric(df_winter['Indoor Mean Air Temperature'])
df_winter['Indoor Air Relative Humidity'] = pd.to_numeric(df_winter['Indoor Air Relative Humidity'])

# Drop missing values
df_winter.dropna(inplace=True)

print('Info about the data set:')
print(df_winter.info())
print('Number of missing values in the data set : \n')
print(df_winter.isnull().sum())


# SUMMER

df_summer = {}
for path in paths_summer:
    try:
        df_summer[path] = pd.read_csv(path_directory_summer + path, header = [0], index_col=[0], encoding='latin1')
        
        df_summer[path]['Datetime'] = df_summer[path]['Date'] + ' ' + df_summer[path]['Time']
        df_summer[path]['Datetime'] = pd.to_datetime(df_summer[path]['Datetime'], format='%m/%d/%Y %H:%M:%S %p')

        key = path[:10]
        try:
            df_summer[path] = df_summer[path][['Datetime', 'Readings (°C)', 'Readings (%RH)']]
        except:
            df_summer[path] = df_summer[path][['Datetime', 'Temp', 'RH']]
        df_summer[path].columns = ['Datetime', 'Indoor Mean Air Temperature', 'Indoor Air Relative Humidity']

        df_summer[path] = df_summer[path].loc[(df_summer[path]['Indoor Air Relative Humidity'] >= 0) & (df_summer[path]['Indoor Air Relative Humidity'] <= 100)]

        df_summer[path]['key'] = key
        df_summer[path]['Season'] = 'Summer'
    except:
        print(path) # Print the name of the file that could not be read
    

# Concatenate all dataframes
df_summer = pd.concat(df_summer, ignore_index=True)

print('Info about the data set:')
print(df_summer.info())


# Clean SUMMER data
strings = df_summer[~df_summer['Indoor Mean Air Temperature'].astype(str).str.contains(r'^-?\d+\.?\d*$')]['Indoor Mean Air Temperature'].unique()
print('Non-numeric values in the data set : {} \n'.format(strings))

df_summer.replace('> 85.0 ', np.nan, inplace=True)

# Convert to numeric
df_summer['Indoor Mean Air Temperature'] = pd.to_numeric(df_summer['Indoor Mean Air Temperature'])
df_summer['Indoor Air Relative Humidity'] = pd.to_numeric(df_summer['Indoor Air Relative Humidity'])

# Drop missing values
df_summer.dropna(inplace=True)

# Delete duplicate key and datetime
df_summer.drop_duplicates(subset=['key', 'Datetime'], inplace=True)
df_winter.drop_duplicates(subset=['key', 'Datetime'], inplace=True)

print('Info about the data set:')
print(df_summer.info())
print('Number of missing values in the data set : \n')
print(df_summer.isnull().sum())


# Common measurements period WINTER
common_period_winter = df_winter.groupby('key')['Datetime'].agg(['min', 'max'])
# Manual input for Winter because 3 dataframes are not in the common period.
date_min_winter = '2017-07-03 00:00:00'
date_max_winter = '2017-09-12 12:00:00'
print('Common period of measurements for WINTER : {} - {}'.format(date_min_winter, date_max_winter))

# Common measurements period SUMMER
common_period_summer = df_summer.groupby('key')['Datetime'].agg(['min', 'max'])
date_min_summer = common_period_summer['min'].max()
date_max_summer = common_period_summer['max'].min()
print('Common period of measurements for SUMMER : {} - {}'.format(date_min_summer, date_max_summer))

# Filter dataframes
df_winter_filtered = df_winter[(df_winter['Datetime'] >= date_min_winter) & (df_winter['Datetime'] <= date_max_winter)]
df_summer_filtered = df_summer[(df_summer['Datetime'] >= date_min_summer) & (df_summer['Datetime'] <= date_max_summer)]

# Create dict of dataframes by key
df_winter_dict = dict(tuple(df_winter_filtered.groupby('key')))
df_summer_dict = dict(tuple(df_summer_filtered.groupby('key')))

print('Info about the data set:')
print('Number of keys in WINTER data set : {}'.format(len(df_winter_dict.keys())))
print('Number of keys in SUMMER data set : {}'.format(len(df_summer_dict.keys())))


# Eject keys with less than 95% of datapoints SUMMER
key_to_eject = None
for key in df_winter_dict.keys():
    if len(df_winter_dict[key]) < (pd.Series([len(df_winter_dict[key]) for key in df_winter_dict.keys()]).value_counts().sort_index(ascending=False).index[0])*0.95:
        key_to_eject = key
    df_winter_dict[key] = df_winter_dict[key].sort_values(by=['Datetime'])
    df_winter_dict[key] = df_winter_dict[key].resample('2H', on='Datetime').mean()
    df_winter_dict[key]['Datetime'] = df_winter_dict[key].index
    df_winter_dict[key]['key'] = key
    
if key_to_eject is not None:
    df_winter_dict.pop(key_to_eject)
df_winter_filtered = pd.concat(df_winter_dict, ignore_index=True)

print('Info about the data set:')
print('Number of keys: {}'.format(len(df_winter_dict)))
print('Key to eject: {}'.format(key_to_eject))


# Eject keys with less than 95% of datapoints SUMMER
key_to_eject = None
for key in df_summer_dict.keys():
    if len(df_summer_dict[key]) < (pd.Series([len(df_summer_dict[key]) for key in df_summer_dict.keys()]).value_counts().sort_index(ascending=False).index[0])*0.95:
        key_to_eject = key
    df_summer_dict[key] = df_summer_dict[key].sort_values(by=['Datetime'])
    df_summer_dict[key] = df_summer_dict[key].resample('1H', on='Datetime').mean()
    df_summer_dict[key]['Datetime'] = df_summer_dict[key].index
    df_summer_dict[key]['key'] = key

if key_to_eject is not None:
    df_summer_dict.pop(key_to_eject)
df_summer_filtered = pd.concat(df_summer_dict, ignore_index=True)

print('Info about the data set:')
print('Number of keys: {}'.format(len(df_summer_dict)))
print('Key to eject: {}'.format(key_to_eject))


# Interpolate missing values

df_temp = df_summer_filtered.pivot_table(values='Indoor Mean Air Temperature', index='Datetime', columns='key')
df_temp = df_temp.interpolate(method='time', limit_direction='both')
df_rh = df_summer_filtered.pivot_table(values='Indoor Air Relative Humidity', index='Datetime', columns='key')
df_rh = df_rh.interpolate(method='time', limit_direction='both')
# Merge dataframes to a dictionary with keys and dataframes of three columns (Datetime, Temperature, Relative Humidity)
df_dict = {}
for key in df_temp.columns:
    df_dict[key] = pd.concat([df_temp[key], df_rh[key]], axis=1)
    df_dict[key].columns = ['Indoor Mean Air Temperature', 'Indoor Air Relative Humidity']
    df_dict[key].index = pd.to_datetime(df_dict[key].index)
df_summer_dict = df_dict


df_temp = df_winter_filtered.pivot_table(values='Indoor Mean Air Temperature', index='Datetime', columns='key')
df_temp = df_temp.interpolate(method='time', limit_direction='both')

df_rh = df_winter_filtered.pivot_table(values='Indoor Air Relative Humidity', index='Datetime', columns='key')
df_rh = df_rh.interpolate(method='time', limit_direction='both')

# Merge dataframes to a dictionary with keys and dataframes of three columns (Datetime, Temperature, Relative Humidity)
df_dict = {}
for key in df_temp.columns:
    df_dict[key] = pd.concat([df_temp[key], df_rh[key]], axis=1)
    df_dict[key].columns = ['Indoor Mean Air Temperature', 'Indoor Air Relative Humidity']
    df_dict[key].index = pd.to_datetime(df_dict[key].index)
df_winter_dict = df_dict


# Merge with weather data

df_weather = pd.read_csv('database/cleaned/giyani_weather.csv', header=0, parse_dates=True)
df_weather['Datetime'] = pd.to_datetime(df_weather['Datetime'])

columns = ['Indoor Mean Air Temperature', 'Indoor Air Relative Humidity', 'Outdoor Dry Bulb Temperature', 'Outdoor Relative Humidity', 'Atmospheric Station Pressure', 'Wind Speed', 'Wind Direction', 'Precipitable Water']
# Merge

for key in df_summer_dict.keys():
    df_summer_dict[key] = pd.merge_asof(df_summer_dict[key].sort_values('Datetime'), df_weather.sort_values('Datetime'), on='Datetime', direction='nearest')
    df_summer_dict[key].set_index('Datetime', inplace=True)
    df_summer_dict[key] = df_summer_dict[key][columns]


for key in df_winter_dict.keys():
    df_winter_dict[key] = pd.merge_asof(df_winter_dict[key].sort_values('Datetime'), df_weather.sort_values('Datetime'), on='Datetime', direction='nearest')
    df_winter_dict[key].set_index('Datetime', inplace=True)
    df_winter_dict[key] = df_winter_dict[key][columns]


# Save data WINTER
for key in df_winter_dict.keys():
    df_winter_dict[key].to_csv('database/cleaned/giyani/winter_{}.csv'.format(key), index=True)

for key in df_winter_dict.keys():
    df_winter_dict[key]['key'] = key
    df_winter_dict[key]['Datetime'] = df_winter_dict[key].index
# Concatenate all dataframes
df_winter = pd.concat(df_winter_dict, ignore_index=True)
df_winter.to_csv('database/cleaned/giyani_winter_concatenated.csv', index=True)


# Save data SUMMER
for key in df_summer_dict.keys():
    df_summer_dict[key].to_csv('database/cleaned/giyani/summer_{}.csv'.format(key), index=True)

for key in df_summer_dict.keys():
    df_summer_dict[key]['key'] = key
    df_summer_dict[key]['Datetime'] = df_summer_dict[key].index
# Concatenate all dataframes
df_summer = pd.concat(df_summer_dict, ignore_index=True)
df_summer.to_csv('database/cleaned/giyani_summer_concatenated.csv', index=True)


SeriesLength = pd.Series([len(df_winter_dict[key]) for key in df_winter_dict.keys()])
SeriesLength.value_counts().sort_index(ascending=False)



SeriesLength = pd.Series([len(df_summer_dict[key]) for key in df_summer_dict.keys()])
SeriesLength.value_counts().sort_index(ascending=False)


# Missing values
print('Missing values in winter:')
print(df_winter.isnull().sum())
print('Missing values in summer:')
print(df_summer.isnull().sum())


