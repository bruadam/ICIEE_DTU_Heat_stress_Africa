from pyosmodel.utils import GaussianRandomValuesPositive, UniformRandomValues
import numpy as np
import pandas as pd

# Define inputs for the simulation of a shack
'''
Description: This function defines the inputs for the simulation of a shack
Inputs:
    - N : the number of shacks to simulate
Outputs:
    - floor_area : the floor area of the shack in m2
    - building_height : the height of the shack in m
    - building_length : the length of the shack in m
    - building_width : the width of the shack in m
    - window_to_wall_ratio : the window to wall ratio of the shack
    - number_people : the number of people in the shack
    - activity_level : the activity level of the people in the shack
    - P_equip : the power of the equipment in the shack in W
    - P_hvac : the power of the HVAC system in the shack in W
    - wall_construction_list : the list of materials used for the wall construction
    - roof_construction_list : the list of materials used for the roof construction
    - floor_construction_list : the list of materials used for the floor construction
    - ground_construction_list : the list of materials used for the ground construction
    - door_height : the height of the door in m
    - door_width : the width of the door in m
    - infiltration_rate : the infiltration rate of the shack in m3/s
    - u_factor : the u-factor of the windows in W/m2K
    - shgc : the solar heat gain coefficient of the windows
    - heating_setpoint : the heating setpoint of the shack
    - orientation : the orientation of the shack in degrees from North (0 to 360)
    - type_house : the type of house Shack
    - lighting_bulbs : the number of light bulbs in the shack
    - elec_gas : the type of equipment system in the shack (Electric or Gas)

'''
def define_shack_inputs(N):
    floor_area = GaussianRandomValuesPositive(25, 5, N)
    building_height = GaussianRandomValuesPositive(2.5, 0.5, N)
    length_width_ratio = GaussianRandomValuesPositive(1, 0.3, N)
    building_length = np.sqrt(floor_area * length_width_ratio)
    building_width = np.sqrt(floor_area / length_width_ratio)
    window_to_wall_ratio = GaussianRandomValuesPositive(0.05, 0.05, N)
    number_people = np.ceil(GaussianRandomValuesPositive(2, 1, N))
    activity_level = GaussianRandomValuesPositive(100, 30, N)
    P_equip = GaussianRandomValuesPositive(100, 50, N)
    P_hvac = GaussianRandomValuesPositive(1500, 300, N)
    # Define the materials
    floor_constructions = [
        [
            ["Wood", 0.05, 0.146, 610, 2385, 0.9, 0.9], # For oak red black wood
        ],
        [
            ["Carpet", 0.013, 0.13, 910, 1925, 0.9, 0.9], # For polypropylene moplin
        ],
    ]

    wall_constructions = [
        [
            ["Wood", 0.05, 0.146, 610, 2385, 0.9, 0.9],
        ],
        [
            ["Corrugated Steel", 0.005, 50, 7850, 500, 0.9, 0.9], 
        ],
    ]

    roof_constructions = [
        [
            ["Wood", 0.05, 0.146, 610, 2385, 0.9, 0.9],
        ],
        [
            ["Corrugated Steel", 0.005, 50, 7850, 500, 0.9, 0.9],
        ],
        [
            ["Wood", 0.05, 0.146, 610, 2385, 0.9, 0.9],
            ["Ceiling Insulation", 0.2, 0.035, 100, 1130, 0.9, 0.9], # Extruded polystyrene rigid foamed in place
        ],
        [
            ["Corrugated Steel", 0.005, 50, 7850, 500, 0.9, 0.9],
            ["Ceiling Insulation", 0.2, 0.035, 100, 1130, 0.9, 0.9], # Extruded polystyrene rigid foamed in place
        ],
        [
            ["Asbestos", 0.02, 0.63, 1850, 1674, 0.9, 0.9], # melamine asbestos
        ],
        [
            ["Asbestos", 0.02, 0.63, 1850, 1674, 0.9, 0.9], # melamine asbestos
            ["Ceiling Insulation", 0.2, 0.035, 100, 1130, 0.9, 0.9], # Extruded polystyrene rigid foamed in place
        ],
    ]
    # Choose a random construction for each shack
    floor_construction_list_index = np.random.randint(0, len(floor_constructions), N)
    wall_construction_list_index = np.random.randint(0, len(wall_constructions), N)
    roof_construction_list_index = np.random.randint(0, len(roof_constructions), N)
    ground_construction_list_index = np.random.randint(0, len(floor_constructions), N)
    # Create the construction lists
    floor_construction_list = [floor_constructions[i] for i in floor_construction_list_index]
    wall_construction_list = [wall_constructions[i] for i in wall_construction_list_index]
    roof_construction_list = [roof_constructions[i] for i in roof_construction_list_index]
    ground_construction_list = [floor_constructions[i] for i in ground_construction_list_index]


    fraction_building_height = UniformRandomValues(0.6, 0.8, N)
    door_width = GaussianRandomValuesPositive(1, 0.5, N)
    infiltration_rate = UniformRandomValues(0.2, 1, N) # 0.2 ACH to 1 ACH
    u_factor = GaussianRandomValuesPositive(2, 0.5, N)
    shgc = UniformRandomValues(0.5, 0.9, N)
    # N values for the heating setpoint of 10 degrees
    heating_setpoint = np.ones(N) * 10
    orientation= np.random.choice(list(range(0,360,45)), N)
    
    # N times "Shack"
    type_house = np.repeat("Shack", N)
    lighting_bulbs = np.ceil(GaussianRandomValuesPositive(3, 1, N))
    elec_gas = np.random.choice(["Electric", "Gas"], N)
    
    # Store the inputs in a dataframe
    inputs = pd.DataFrame({"floor_area": floor_area, "building_height": building_height, "building_length": building_length, "building_width": building_width, "window_to_wall_ratio": window_to_wall_ratio, "number_people": number_people, "activity_level": activity_level, "P_equip": P_equip, "P_hvac": P_hvac, "wall_construction_list": wall_construction_list, "roof_construction_list": roof_construction_list, "floor_construction_list": floor_construction_list, "ground_construction_list": ground_construction_list, "door_height_fraction_building_height": fraction_building_height, "door_width": door_width, "infiltration_rate": infiltration_rate, "u_factor": u_factor, "shgc": shgc, "heating_setpoint": heating_setpoint, "orientation": orientation, "type_house": type_house, "lighting_bulbs": lighting_bulbs, "elec_gas": elec_gas})

    return inputs
# Define a function for the inputs of a RDP
'''
Description: This function defines the inputs for the simulation of a RDP
Inputs:
    - N : the number of RDPs to simulate
Outputs:
    - floor_area : the floor area of the RDP in m2
    - building_height : the height of the RDP in m
    - building_length : the length of the RDP in m
    - building_width : the width of the RDP in m
    - window_to_wall_ratio : the window to wall ratio of the RDP
    - number_people : the number of people in the RDP
    - activity_level : the activity level of the people in the RDP
    - P_equip : the power of the equipment in the RDP in W
    - P_hvac : the power of the HVAC system in the RDP in W
    - wall_construction_list : the list of materials used for the wall construction
    - roof_construction_list : the list of materials used for the roof construction
    - floor_construction_list : the list of materials used for the floor construction
    - ground_construction_list : the list of materials used for the ground construction
    - door_height : the height of the door in m
    - door_width : the width of the door in m
    - infiltration_rate : the infiltration rate of the RDP in m3/s
    - u_factor : the u-factor of the windows in W/m2K
    - shgc : the solar heat gain coefficient of the windows
    - heating_setpoint : the heating setpoint of the RDP
    - orientation : the orientation of the RDP in degrees from North (0 to 360)
    - type_house : the type of house RDP
    - lighting_bulbs : the number of light bulbs in the RDP
    - elec_gas : the type of equipment system in the RDP (Electric or Gas)

'''
def define_RDP_inputs(N):
    floor_area = GaussianRandomValuesPositive(50, 10, N)
    building_height = GaussianRandomValuesPositive(3, 0.5, N)
    length_width_ratio = GaussianRandomValuesPositive(1, 0.2, N)
    building_length = np.sqrt(floor_area * length_width_ratio)
    building_width = np.sqrt(floor_area / length_width_ratio)
    window_to_wall_ratio = GaussianRandomValuesPositive(0.1, 0.05, N)
    number_people = np.ceil(GaussianRandomValuesPositive(5, 2, N))
    activity_level = GaussianRandomValuesPositive(100,50, N)
    P_equip = GaussianRandomValuesPositive(100, 100, N)
    P_hvac = GaussianRandomValuesPositive(1500, 500, N)
    # Define the materials
    floor_constructions = [
        [   
            ["Carpet", 0.013, 0.13, 910, 1925, 0.9, 0.9], # For polypropylene moplin
            ["Concrete", 0.1, 0.209, 950, 657, 0.9, 0.9], # concrete lightweight
        ],
        [
            ["Concrete", 0.1, 0.209, 950, 657, 0.9, 0.9], # concrete lightweight
        ],
        [
            ["Wood", 0.05, 0.146, 610, 2385, 0.9, 0.9], # For oak red black wood
            ["Concrete", 0.1, 0.209, 950, 657, 0.9, 0.9], # concrete lightweight
        ],
        [
            ["Ceramic Tile", 0.013, 0.9, 2240, 880, 0.9, 0.9],
            ["Concrete", 0.1, 0.209, 950, 657, 0.9, 0.9], # concrete lightweight
        ],
    ]

    wall_constructions = [
        [
            ["Brick", 0.15, 0.711, 2000, 837, 0.9, 0.9], # brick masonry medium
        ],
        [
            ["Concrete", 0.1, 0.335, 1600, 657, 0.9, 0.9], # concrete cinder
        ],
    ]

    roof_constructions = [
        [
            ["Wood", 0.05, 0.146, 610, 2385, 0.9, 0.9], # For oak red black wood
        ],
        [
            ["Concrete", 0.1, 0.209, 950, 657, 0.9, 0.9], # concrete lightweight
        ],
        [
            ["Corrugated Steel", 0.005, 50, 7850, 500, 0.9, 0.9],
        ],
        [
            ["Wood", 0.05, 0.146, 610, 2385, 0.9, 0.9], # For oak red black wood
            ["Ceiling Insulation", 0.2, 0.035, 100, 1130, 0.9, 0.9], # Extruded polystyrene rigid foamed in place
        ],
        [
            ["Concrete", 0.1, 0.209, 950, 657, 0.9, 0.9], # concrete lightweight
            ["Ceiling Insulation", 0.2, 0.035, 100, 1130, 0.9, 0.9], # Extruded polystyrene rigid foamed in place
        ],
        [
            ["Corrugated Steel", 0.005, 50, 7850, 500, 0.9, 0.9],
            ["Ceiling Insulation", 0.2, 0.035, 100, 1130, 0.9, 0.9], # Extruded polystyrene rigid foamed in place
        ],
        [
            ["Clay Tile", 0.02, 1.0, 2000, 753, 0.9, 0.9], # missouri fireclay brick
        ],
        [
            ["Clay Tile", 0.02, 1.0, 2000, 753, 0.9, 0.9], # missouri fireclay brick
            ["Ceiling Insulation", 0.2, 0.035, 100, 1130, 0.9, 0.9], # Extruded polystyrene rigid foamed in place
        ],
        [
            ["Asbestos", 0.02, 0.63, 1850, 1674, 0.9, 0.9], # melamine asbestos
        ],
        [
            ["Asbestos", 0.02, 0.63, 1850, 1674, 0.9, 0.9], # melamine asbestos
            ["Ceiling Insulation", 0.2, 0.035, 100, 1130, 0.9, 0.9], # Extruded polystyrene rigid foamed in place
        ],
    ]
    # Choose a random construction for each shack
    floor_construction_list_index = np.random.randint(0, len(floor_constructions), N)
    wall_construction_list_index = np.random.randint(0, len(wall_constructions), N)
    roof_construction_list_index = np.random.randint(0, len(roof_constructions), N)
    ground_construction_list_index = np.random.randint(0, len(floor_constructions), N)
    # Create the construction lists
    floor_construction_list = [floor_constructions[i] for i in floor_construction_list_index]
    wall_construction_list = [wall_constructions[i] for i in wall_construction_list_index]
    roof_construction_list = [roof_constructions[i] for i in roof_construction_list_index]
    ground_construction_list = [floor_constructions[i] for i in ground_construction_list_index]


    fraction_building_height = UniformRandomValues(0.7, 0.8, N)
    door_width = GaussianRandomValuesPositive(1, 0.1, N)
    infiltration_rate = UniformRandomValues(0.2, 0.5, N) # 0.2 ACH to 0.5 ACH
    u_factor = GaussianRandomValuesPositive(1.3, 0.3, N)
    shgc = UniformRandomValues(0.5, 0.7, N)
    heating_setpoint = np.ones(N) * 10
    orientation= np.random.choice(list(range(0,360,45)), N)
    type_house = np.repeat("RDP", N)
    lighting_bulbs = np.ceil(GaussianRandomValuesPositive(3, 1, N))
    elec_gas = np.random.choice(["Electric", "Gas"], N)

    # Store values in a dataframe
    inputs = pd.DataFrame({"floor_area": floor_area, "building_height": building_height, "building_length": building_length, "building_width": building_width, "window_to_wall_ratio": window_to_wall_ratio, "number_people": number_people, "activity_level": activity_level, "P_equip": P_equip, "P_hvac": P_hvac, "wall_construction_list": wall_construction_list, "roof_construction_list": roof_construction_list, "floor_construction_list": floor_construction_list, "ground_construction_list": ground_construction_list, "door_height_fraction_building_height": fraction_building_height, "door_width": door_width, "infiltration_rate": infiltration_rate, "u_factor": u_factor, "shgc": shgc, "heating_setpoint": heating_setpoint, "orientation": orientation, "type_house": type_house, "lighting_bulbs": lighting_bulbs, "elec_gas": elec_gas})

    return inputs