import openstudio as op
import pandas as pd
import os
from openstudio import openstudioutilities as osu
from epw import epw
from datetime import datetime

# Definition to set up the models and units of the model
'''
Description: This function sets up the models and units of the model. The function returns a model, which can be used to create a building.
Input: None
Output: op.model.Model
'''
def setup_model(epw_path):
    # Create a model
    model = op.model.Model()

    epw_file = op.path(epw_path)
    epw_file = osu.openstudioutilitiesfiletypes.EpwFile(epw_file)

    # Define the units
    op.UnitSystem("SI")
    model.setDayofWeekforStartDay("Monday")
    model.setCalendarYear(2023)

    # Define the weather file
    weather_file = model.getWeatherFile()
    weather_file.setWeatherFile(model, epw_file)

    return model

# Definition to set up the building
'''
Description: This function sets up the building with a given floor to floor height, orientation and space type. The function returns a space, thermal zone and building story instance, which can be used to create a model.
Input:
- model: op.model.Model
- floor_to_floor_height: float in m
- orientation: float in degrees
- space_type: string
Output: space, thermal_zone, building_story
'''
def setup_building(model, floor_to_floor_height, orientation, space_type):
    # Define the building
    building = model.getBuilding()
    building.setName("Building")
    building.setNorthAxis(op.degToRad(float(orientation)))

    # Define the thermal zone
    thermal_zone = op.model.ThermalZone(model)
    thermal_zone.setName("Thermal Zone")
    thermal_zone.setMultiplier(1)

    # Define the space
    space = op.model.Space(model)
    space.setName("Space")
    space.setThermalZone(thermal_zone)
    space_type_instance = op.model.SpaceType(model)
    space_type_instance.setStandardsSpaceType(space_type)
    space.setSpaceType(space_type_instance)

    # Define the building story
    building_story = op.model.BuildingStory(model)
    building_story.setName("Story")
    building_story.setNominalFloortoCeilingHeight(floor_to_floor_height)
    building_story.setNominalZCoordinate(0)

    return space, thermal_zone, building_story

# Definition to import a weather file
'''
Description: This function imports a weather file into the model
Inputs:
    model: the model to import the weather file into
    epw_path: the path to the weather file
Outputs:
    weather: the weather file object
'''
def import_epw(model, epw_path):
    model_year = model.getYearDescription().calendarYear()
    # Import the weather file
    weather = pd.DataFrame()
    df = epw()
    df.read(epw_path)
    location = df.headers['LOCATION']
    df = df.dataframe
    # Create the weather DataFrame
    weather = pd.DataFrame(df, columns=['Year', 'Month', 'Day', 'Hour', 'Minute', 'Dry Bulb Temperature', 'Dew Point Temperature', 'Relative Humidity', 'Wind Speed', 'Wind Direction', 'Global Horizontal Radiation', 'Diffuse Horizontal Radiation', 'Direct Normal Radiation', 'Diffuse Horizontal Illuminance', 'Direct Normal Illuminance', 'Total Sky Cover', 'Precipitable Water'])

    # Convert the weather date to a datetime object
    # Change the year to the model year
    weather['Year'] = model_year
    weather['Hour'] = weather['Hour'].replace(24, 0)
    weather['Minute'] = weather['Minute'].replace(60, 0)
    weather['Datetime'] = weather.apply(lambda row: datetime(int(row['Year']), int(row['Month']), int(row['Day']), int(row['Hour']), int(row['Minute']), 0), axis=1)

    # Set the weather date as the index
    weather = weather.set_index('Datetime')
    weather.drop(['Year', 'Month', 'Day', 'Hour', 'Minute'], axis=1, inplace=True)
    return weather, location
   