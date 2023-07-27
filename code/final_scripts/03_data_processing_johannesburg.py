# Author: Bruno Marc J. Adam
# Last Update: 2023-07-03
# Purpose: Script to data processing of the measurements data from Johannesburg, South Africa

# University: DTU
# Master Thesis Project: Using AI to predict thermal comfort in buildings in South Africa

# Import libraries
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')


# Import data
path = '..\database\johannesburg\Jhb_Indoor_Housing_Temp_Data.xlsx'

keys = pd.ExcelFile(path).sheet_names
df = pd.read_excel(path, sheet_name=keys)

for key in keys:
    df[key]['Datetime'] = pd.to_datetime(df[key]['Date'].astype(str) + ' ' + df[key]['Time'].astype(str))
    df[key] = df[key][['Datetime', 'Readings (°C)', 'Readings (%RH)']]
    df[key].rename(columns={'Readings (°C)': 'Indoor Mean Air Temperature', 'Readings (%RH)': 'Indoor Air Relative Humidity'}, inplace=True)
    df[key]['key'] = key
df = pd.concat(df, ignore_index=True)

print('Info about the data set:')
print(df.info())


# Clean data
strings = df[~df['Indoor Mean Air Temperature'].astype(str).str.contains(r'^-?\d+\.?\d*$')]['Indoor Mean Air Temperature'].unique()
print('Non-numeric values in the data set : {} \n'.format(strings))

df.replace('> 85.0  ', np.nan, inplace=True) # Replace strings with NaN

# Convert columns to numeric
df['Indoor Mean Air Temperature'] = pd.to_numeric(df['Indoor Mean Air Temperature'])
df['Indoor Air Relative Humidity'] = pd.to_numeric(df['Indoor Air Relative Humidity'])

# Drop missing values
df.dropna(inplace=True)

print('Info about the data set:')
print(df.info())


# Common measurements period
common_datetime_range = df.groupby('key')['Datetime'].agg(['min', 'max'])
date_min = common_datetime_range['min'].max()
date_max = common_datetime_range['max'].min()
print('Common datetime range: {} - {} \n'.format(date_min, date_max))

# Filter data
df_filtered = df[(df['Datetime'] >= date_min) & (df['Datetime'] <= date_max)]

# Create a dict with keys and dataframes
df_dict = dict(tuple(df_filtered.groupby('key')))


print('Info about the data set:')
print('Number of keys: {}'.format(len(df_dict)))


# Eject keys with less than 95% of the data points
for key in df_dict.keys():
    if len(df_dict[key]) < (pd.Series([len(df_dict[key]) for key in df_dict.keys()]).value_counts().sort_index(ascending=False).index[0])*0.95:
        key_to_eject = key
    df_dict[key] = df_dict[key].sort_values(by=['Datetime'])
    df_dict[key] = df_dict[key].resample('1H', on='Datetime').mean()
    df_dict[key]['Datetime'] = df_dict[key].index
    df_dict[key]['key'] = key

df_dict.pop(key_to_eject)
df_filtered = pd.concat(df_dict, ignore_index=True)

print('Info about the data set:')
print('Number of keys: {}'.format(len(df_dict)))
print('Key to eject: {}'.format(key_to_eject))


# Interpolate missing values

df_temp = df_filtered.pivot_table(values='Indoor Mean Air Temperature', index='Datetime', columns='key')
df_temp = df_temp.interpolate(method='time', limit_direction='both')

df_rh = df_filtered.pivot_table(values='Indoor Air Relative Humidity', index='Datetime', columns='key')
df_rh = df_rh.interpolate(method='time', limit_direction='both')

# Merge dataframes to a dictionary with keys and dataframes of three columns (Datetime, Temperature, Relative Humidity)
df_dict = {}
for key in df_temp.columns:
    df_dict[key] = pd.concat([df_temp[key], df_rh[key]], axis=1)
    df_dict[key].columns = ['Indoor Mean Air Temperature', 'Indoor Air Relative Humidity']
    df_dict[key].index = pd.to_datetime(df_dict[key].index)


# Merge with weather data

df_weather = pd.read_csv('database/cleaned/johannesburg_weather.csv', header=0, parse_dates=True)
df_weather['Datetime'] = pd.to_datetime(df_weather['Datetime'])
df_weather.set_index('Datetime', inplace=True)

columns = ['Indoor Mean Air Temperature', 'Indoor Air Relative Humidity', 'Outdoor Dry Bulb Temperature', 'Outdoor Relative Humidity', 'Atmospheric Station Pressure', 'Wind Speed', 'Wind Direction', 'Precipitable Water']
# Merge
for key in df_dict.keys():
    df_dict[key] = pd.merge_asof(df_dict[key], df_weather, left_on='Datetime', right_on='Datetime', direction='nearest')
    df_dict[key].set_index('Datetime', inplace=True)
    df_dict[key] = df_dict[key][columns]


# Save data 
for key in df_dict.keys():
    df_dict[key].to_csv('database/cleaned/johannesburg/{}.csv'.format(key), index=True)

for key in df_dict.keys():
    df_dict[key]['key'] = key
    df_dict[key]['Datetime'] = df_dict[key].index
# Concatenate all dataframes
df = pd.concat(df_dict, ignore_index=True)
df.to_csv('database/cleaned/johannesburg_concatenated.csv', index=True)


