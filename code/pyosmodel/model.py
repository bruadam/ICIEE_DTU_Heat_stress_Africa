import numpy as np
from datetime import datetime, timedelta, time

from pyosmodel.origin import setup_model, setup_building
from pyosmodel.geometry import create_geometry_box
from pyosmodel.construction import create_material_list, create_construction, assign_construction, create_window_construction
from pyosmodel.schedule import set_occupancy_schedule, set_activity_level_schedule, set_equipment_schedule, set_heating_set_point_schedule, set_schedule_always_on_off, set_lighting_schedule
from pyosmodel.internal_loads import add_people, add_lighting, add_electric_equipment, add_gas_equipment
from pyosmodel.hvac import add_coil_heater, add_infiltration
from pyosmodel.output import set_output_variables
from pyosmodel.params import setup_simulation_control
from pyosmodel.subsurface import create_door

import openstudio as op

# Define a function to set up a full model
'''
Description: This function set up a full model
Inputs:
    - input_data: dictionary with the following keys:
        - building_length: float in m
        - building_width: float in m
        - building_height: float in m
        - door_height_fraction_building_height: float between 0 and 1
        - orientation: float in degrees
        - wall_construction_list: list of strings
        - roof_construction_list: list of strings
        - floor_construction_list: list of strings
        - ground_construction_list: list of strings
        - window_to_wall_ratio: float between 0 and 1
        - u_factor: float in W/m2K
        - shgc: float between 0 and 1
        - number_people: float
        - floor_area: float in m2
        - activity_level: float
        - infiltration_rate: float in m3/s
        - P_equip: float in W
        - P_hvac: float in W
        - heating_setpoint: float in degrees Celsius
        - door_width: float in m
    - output_data: dictionary with the following keys:
        - output_variables: list of strings
    - sunhours_path: string

Outputs:
    - model: op.model.Model
'''
def simulate_model(input_data, output_data, epw_path):
    # Input data
    building_length = input_data['building_length']
    building_width = input_data['building_width']
    building_height = input_data['building_height']
    fraction_building_height = input_data['door_height_fraction_building_height']
    orientation = input_data['orientation']
    wall_construction_list = input_data['wall_construction_list']
    roof_construction_list = input_data['roof_construction_list']
    floor_construction_list = input_data['floor_construction_list']
    ground_construction_list = input_data['ground_construction_list']
    window_to_wall_ratio = input_data['window_to_wall_ratio']
    u_factor = input_data['u_factor']
    shgc = input_data['shgc']
    number_people = input_data['number_people']
    floor_area = input_data['floor_area']
    activity_level = input_data['activity_level']
    infiltration_rate = input_data['infiltration_rate']
    P_equip = input_data['P_equip']
    P_hvac = input_data['P_hvac']
    heating_setpoint = input_data['heating_setpoint']
    door_width = input_data['door_width']
    lighting_bulbs = input_data['lighting_bulbs']
    elec_gas = input_data['elec_gas']
    
    # Set up the model
    model = setup_model(epw_path)

    orientation = float(orientation * np.pi / 180)
    # Set up the building
    space, thermal_zone, building_story = setup_building(model, building_height, orientation, "RDP - House")

    # Create a box
    create_geometry_box(model, space, building_length, building_width, building_height)

    # Create construction sets
    wall_construction_list = create_material_list(model, wall_construction_list)
    wall_construction = create_construction(model, "Wall Construction", wall_construction_list)
    roof_construction_list = create_material_list(model, roof_construction_list)
    roof_constructions = create_construction(model, "Roof Construction", roof_construction_list)
    floor_construction_list = create_material_list(model, floor_construction_list)
    floor_construction = create_construction(model, "Floor Construction", floor_construction_list)
    ground_construction_list = create_material_list(model, ground_construction_list)
    ground_construction = create_construction(model, "Ground Construction", ground_construction_list)

    # Assign the construction to the surfaces that are walls
    surfaces = space.surfaces()
    for surface in surfaces:
        if surface.surfaceType() == "Wall":
            assign_construction(surface, wall_construction)
        if surface.surfaceType() == "RoofCeiling":
            assign_construction(surface, roof_constructions)
        if surface.surfaceType() == "Floor":
            assign_construction(surface, floor_construction)
        if surface.surfaceType() == "Ground":
            assign_construction(surface, ground_construction)

    # Create a door for a random surface  which is a wall
    wall_surfaces = [surface for surface in surfaces if surface.surfaceType() == "Wall"]
    door_surface = np.random.choice(wall_surfaces)
    door = create_door(model, door_surface, fraction_building_height, door_width, 0.6, 0.05, building_height) # 0.6 W/m2K, 0.05 m thickness is a good assumption for a door made of solid wood for outdoor use
    
    # Create a window construction
    window_construction = create_window_construction(model, u_factor, shgc)

    # Create a central window on each wall surfaces exept the door surface
    for surface in wall_surfaces:
        surface.setWindowToWallRatio(window_to_wall_ratio)
        subsurfaces = surface.subSurfaces()
        for subsurface in subsurfaces:
            if subsurface.subSurfaceType() == "FixedWindow":
                assign_construction(subsurface, window_construction)

    # Occupancy schedule
    occupancy_schedule = set_occupancy_schedule(model)

    # Create a activity level schedule
    activity_level_schedule = set_activity_level_schedule(model, activity_level)
    
    # Add people 
    people_per_area = number_people / floor_area
    people_instance = add_people(model, space, people_per_area, 0.5, occupancy_schedule, activity_level_schedule)

    # Add infiltration
    infiltration = add_infiltration(model, space, infiltration_rate, set_schedule_always_on_off(model, True))

    # # Add lighting schedule
    lighting_schedule = set_lighting_schedule(model)
    # Add lighting
    lighting_per_area = lighting_bulbs*100/floor_area # - Total lighting area (W/m2)
    lighting_instance = add_lighting(model, space, lighting_per_area, lighting_schedule)

    ## EQUIPMENT ##
    # Equipment schedule
    start_time = time(18, 0, 0)
    duration = timedelta(minutes=30)
    equipment_schedule = set_equipment_schedule(model, start_time, duration)
    # Electric equipment
    # Parameters
    P_equip_per_area = P_equip / floor_area # - Total equipment power per area (W/m2)
    if elec_gas == 'Gas':
        gas_equipment_instance = add_gas_equipment(model, space, P_equip_per_area, equipment_schedule)
    elif elec_gas == 'Electric':
        electric_equipment_instance = add_electric_equipment(model, space, P_equip_per_area, equipment_schedule)
    
    # Heater Coil
    # Parameters
    NominalPower = P_hvac # - Nominal power of the heater coil (W)
    heating_setpoint_schedule = set_heating_set_point_schedule(model, heating_setpoint)
    coil_heater = add_coil_heater(model, thermal_zone, NominalPower, heating_setpoint_schedule)

    ## OUTPUTS ## 
    model = set_output_variables(model, output_data)

    # Set up the simulation control
    simulation_start = datetime(2023, 1, 1)
    simulation_end = datetime(2023, 12, 31)
    simulation_control, run_period = setup_simulation_control(model, simulation_start, simulation_end)

    return model

