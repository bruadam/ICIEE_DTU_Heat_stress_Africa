from epw import epw
from pyosmodel.utils import convert_hour_to_datetime


# Define a function to import weather from epw file
'''
Description: This function imports weather from epw file
Input: path of epw file
Output: weather data
'''
def import_epw(path):
    a = epw()
    a.read(path)
    weather = a.dataframe
    weather = weather[['Dry Bulb Temperature', 'Relative Humidity', 'Atmospheric Station Pressure', 'Wind Direction', 'Wind Speed', 'Precipitable Water']]
    # Rename columns
    weather.columns = ['Outdoor Dry Bulb Temperature', 'Outdoor Relative Humidity', 'Atmospheric Station Pressure', 'Wind Direction', 'Wind Speed', 'Precipitable Water']
    weather['datetime'] = weather.index
    for i in range(len(weather['datetime'])):
      weather['datetime'][i] = convert_hour_to_datetime(int(weather['datetime'][i]), 2023)
    weather = weather.set_index('datetime')

    return weather