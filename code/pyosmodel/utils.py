import numpy as np
import openstudio as op
from datetime import datetime, timedelta
import os
import shutil


# Definition of the function to get the surface normal vector
'''
Description: This function gets the outward normal vector of a surface.
Inputs:
    - surface: OpenStudio surface object
Outputs:
    - normal_vector: outward normal vector of the surface
    - unit_vector: unit vector of the surface
'''
def get_surface_normal_vector(surface):
    # Get the outward normal vector of the surface
    normal_vector = surface.outwardNormal()

    # Extract the X, Y, and Z components of the normal vector
    x_component = normal_vector.x()
    y_component = normal_vector.y()
    z_component = normal_vector.z()

    # Create a unit vector
    magnitude = normal_vector.length()
    unit_vector = op.Vector3d(x_component / magnitude, y_component / magnitude, z_component / magnitude)

    return normal_vector, unit_vector

# Definition to calculate the center point of a surface
'''
Description: This function calculates the center point of a given surface
Inputs:
    surface: op.model.Surface
Outputs:
    center_point: op.Point3d
'''
def calculate_center_point(surface):
    # Get the vertices of the surface
    surface_vertices = surface.vertices()

    # Calculate the average of the x, y, and z coordinates of the vertices
    x_sum = 0
    y_sum = 0
    z_sum = 0
    num_vertices = 0

    for vertex in surface_vertices:
        x_sum += vertex.x()
        y_sum += vertex.y()
        z_sum += vertex.z()
        num_vertices += 1

    center_x = x_sum / num_vertices
    center_y = y_sum / num_vertices
    center_z = z_sum / num_vertices

    # Create the center point using the calculated x, y, and z coordinates
    center_point = op.Point3d(center_x, center_y, center_z)

    return center_point

# Definition of the function to rotate the model
'''
Description: This function rotates the model by a given angle.
Inputs:
    - model: OpenStudio model object
    - rotation_angle: angle to rotate the model
Outputs:
    - model: OpenStudio model object with rotated objects
'''
def rotate_model(model, rotation_angle):
    # Get the building rotation angle (angle to rotate the north axis)
    rotation_angle_rad = op.degToRad(rotation_angle)

    # Get the building origin
    origin = op.Point3d(0, 0, 0)

    # Rotate each individual object in the model
    for obj in model.objects():
        if isinstance(obj, op.model.Space):
            # Rotate Spaces
            obj.rotate(origin, op.Vector3d(0, 0, 1), rotation_angle_rad)
        elif isinstance(obj, op.model.ShadingSurface):
            # Rotate Shading Surfaces
            obj.rotate(origin, op.Vector3d(0, 0, 1), rotation_angle_rad)
        # Add more conditions for other object types if needed

    return model

# Definition of the function to fix the schedule type limits of all schedules in the model
'''
Description: This function fixes the schedule type limits of all schedules in the model.
Inputs:
    - model: OpenStudio model object
Outputs:
    - model: OpenStudio model object with fixed schedule type limits
'''
def fix_schedule(model):
    
    # Create a schedule type limits object
    schedule_type_limits = op.model.ScheduleTypeLimits(model)
    schedule_type_limits.setName("My Schedule Type Limits")
    # Set other properties of the schedule type limits as needed

    # Find the schedule objects in the model
    schedules = model.getSchedules()

    # Assign the schedule type limits to the schedules
    for schedule in schedules:
        schedule.setScheduleTypeLimits(schedule_type_limits)

    return model


# Defintion of the function to generate random values from a normal distribution
'''
Description: This function generates N random values from a normal distribution with a given mean and standard deviation.
Inputs:
    - mean: mean of the distribution
    - std: standard deviation of the distribution
    - N: number of random values to generate
Outputs:
    - random_number: N random values from a normal distribution with a given mean and standard deviation
'''
def GaussianRandomValues(mean, std, N):
    return np.random.normal(mean, std, int(N))

# Definition of the function to generate random values from a normal distribution with positive values only
'''
Description: This function generates N random values from a normal distribution with a given mean and standard deviation.
             The generated values are positive only.
Inputs:
    - mean: mean of the distribution
    - std: standard deviation of the distribution
    - N: number of random values to generate
Outputs:
    - random_number: N random values from a normal distribution with a given mean and standard deviation
'''
def GaussianRandomValuesPositive(mean, std, N):
    # Generate a random number
    random_number = np.random.normal(mean, std, int(N))
    # If the random number is negative, make it positive
    random_number[random_number < 0] = -random_number[random_number < 0]
    return random_number

# Definition of the function to generate random values from a uniform distribution
'''
Description: This function generates N random values from a uniform distribution with a given lower and upper bound.
Inputs:
    - low: lower bound of the distribution
    - high: upper bound of the distribution
    - N: number of random values to generate
Outputs:
    - random_number: N random values from a uniform distribution with a given lower and upper bound
'''
def UniformRandomValues(low, high, N):
    return np.random.uniform(low, high, int(N))

# Definition of the function to generate random values from a categorical distribution
'''
Description: This function generates N random values from a categorical distribution with a given set of values.
Inputs:
    - values: set of values to choose from
    - N: number of random values to generate
Outputs:
    - random_number: N random values from a categorical distribution with a given set of values
'''
def CategoricalRandomValues(values, N):
    return np.random.choice(values, int(N))

# Definition of the function to convert hour to datetime
'''
Description: This function converts an hour value to a datetime object using a base date (year, month, day).
Inputs:
    - hour: hour value to convert
    - year: year value to use in the datetime object
    - month: month value to use in the datetime object
    - day: day value to use in the datetime object
Outputs:
    - result: datetime object
'''
def convert_hour_to_datetime(hour, year=2020, month=1, day=1):
    base_date = datetime(year=year, month=month, day=day)  # Choose a base date
    time_delta = timedelta(hours=hour)
    result = base_date + time_delta
    return result

# Definiton of a function to return a op.time object from a datetime.time object
'''
Description: This function converts a datetime.time object to a op.time object.
Inputs:
    - time: datetime.time object
Outputs:
    - op_time: op.time object
'''

def get_op_time(time):
    return op.Time(0, time.hour, time.minute, time.second)

# Definition of a function to return a start and end time from a start time and duration
'''
Description: This function returns a start and end time from a start time and duration.
Inputs:
    - start_time: start time as a datetime.time object
    - duration: duration as a datetime.timedelta object
Outputs:
    - start_time: start time as a datetime.time object
    - end_time: end time as a datetime.time object
'''
def get_start_end_time(start_time, duration):
    now = datetime.now()
    curent_date = now.date()
    year = curent_date.year
    month = curent_date.month
    day = curent_date.day

    start_datetime = datetime(year, month, day, start_time.hour, start_time.minute, start_time.second)
    end_datetime = start_datetime + duration

    start_time = start_datetime.time()
    end_time = end_datetime.time()
    
    return start_time, end_time

# Define the surface plane coordinates
'''
Description: Creates a list of X and Y coordinates for a given surface
Inputs:
    surface: op.model.Surface
Outputs:
    x_coordinates: list of float
    y_coordinates: list of float
'''
def get_surface_plane_coordinates(surface):
    # Get the vertices of the surface
    vertices = surface.vertices()

    # Extract the X and Y coordinates
    x_coordinates = [vertex.x() for vertex in vertices]
    y_coordinates = [vertex.y() for vertex in vertices]
    z_coordinates = [vertex.z() for vertex in vertices]

    return x_coordinates, y_coordinates, z_coordinates

# Definition to clean and set the folders for the simulation
def output_directory(directory_path):
    # Create a folder for the simulation
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
    if not os.path.exists(directory_path + '/models'):
        os.mkdir(directory_path + '/models')
    if os.path.exists(directory_path + '/outputs'):
        shutil.rmtree(directory_path + '/outputs')
    if not os.path.exists(directory_path + '/outputs'):
        os.mkdir(directory_path + '/outputs')
    # Empty the folders
    for file in os.listdir(directory_path + '/models'):
        os.remove(directory_path + '/models/' + file)

# Definition to save the model to IDF format
'''
Description: This function saves the model to IDF format
Input:
- model: op.model.Model
- idf_path: str
'''
def save_model_to_idf(model, idf_path):
    # Save the model to IDF format
    ft = op.energyplus.ForwardTranslator()
    w = ft.translateModel(model)
    w.save(op.path(idf_path), True)

# Definition to calculate U-value given a list of materials and thicknesses
'''
Description: This function calculates the U-value given a list of materials and thicknesses
Inputs:
    - materials: list of op.model.Material
    - thicknesses: list of float
Outputs:
    - U_value: float
'''
def calculate_U_value(materials, thicknesses):
    # Calculate the U-value
    U_value = 0
    for material, thickness in zip(materials, thicknesses):
        U_value += thickness / material.thermalConductivity()
    U_value = 1 / U_value
    return U_value

import os
import subprocess

def clear_screen():
    subprocess.call('clear' if os.name == 'posix' else 'cls', shell=True)
