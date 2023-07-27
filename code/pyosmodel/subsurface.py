import openstudio as op
from pyosmodel.geometry import create_window_vertices, calculate_door_vertices
import math

# Define a central window for a surface
'''
Description: Creates a central window for a surface with a given window to wall ratio, shading factor and window construction
Inputs:
    model: op.model.Model
    surface: op.model.Surface
    window_to_wall_ratio: float in range [0, 1]
    shading_factor: float in range [0, 1]
    window_construction: op.model.Construction
Outputs:
    window: op.model.SubSurface
'''
def create_central_window(model, surface, window_to_wall_ratio, shading_factor, window_construction):
    surface_area = surface.netArea()
    surface_vertices = list(surface.vertices())
    surface_width = (surface_vertices[0] - surface_vertices[1]).length()
    surface_height = (surface_vertices[1] - surface_vertices[2]).length()

    window_area = surface_area * window_to_wall_ratio
    window_side_length = math.sqrt(window_area)
    
    if window_side_length > surface_width or window_side_length > surface_height:
        raise ValueError("The window side length is larger than the surface width or height. Surface name = " + str(surface.name().get()) + ". Window side length = " + str(window_side_length) + ". Surface width = " + str(surface_width) + ". Surface height = " + str(surface_height))

    # Get the center point of the surface
    center_point = op.Point3d(surface_width / 2, surface_height / 2, 0)

    window_vertices = create_window_vertices(surface, center_point, window_side_length, window_side_length)

    window = op.model.SubSurface(window_vertices, model)
    window.setConstruction(window_construction)
    window.setName(surface.name().get() + " Window")
    window.setSurface(surface)
    window.setSubSurfaceType("FixedWindow")

    return window

# Define two windows centered on the left and right side of the surface
'''
Description: Creates two windows centered on the left and right side of the surface with a given window to wall ratio, shading factor and window construction
Inputs:
    model: op.model.Model
    surface: op.model.Surface
    window_to_wall_ratio: float in range [0, 1]
    shading_factor: float in range [0, 1]
    window_construction: op.model.Construction
Outputs:
    window_left: op.model.SubSurface
    window_right: op.model.SubSurface
'''
def create_two_windows(model, surface, window_to_wall_ratio, shading_factor, window_construction):
    surface_area = surface.netArea() 
    surface_vertices = list(surface.vertices())
    surface_width = (surface_vertices[0] - surface_vertices[1]).length()
    surface_height = (surface_vertices[1] - surface_vertices[2]).length()
    
    window_area = surface_area * window_to_wall_ratio
    window_side_length = math.sqrt(window_area/2)
    if 2 * window_side_length > surface_width or window_side_length > surface_height:
        raise ValueError("The window side length is larger than the surface width or height. Surface name = " + str(surface.name().get()) + ". Window side length = " + str(window_side_length) + ". Surface width = " + str(surface_width) + ". Surface height = " + str(surface_height))	
    
    # Position two centered windows on the left and right side of the surface
    # Get two center points on the half left and half right side of the surface
    center_left = op.Point3d(surface_width / 4, surface_height / 2, 0)
    center_right = op.Point3d(surface_width * 3 / 4, surface_height / 2, 0)

    window_vertices_left = create_window_vertices(surface, center_left, window_side_length, window_side_length)
    window_vertices_right = create_window_vertices(surface, center_right, window_side_length, window_side_length)

    window_left = op.model.SubSurface(window_vertices_left, model)
    window_left.setConstruction(window_construction)
    window_left.setName(surface.name().get() + " Window Left")
    window_left.setSurface(surface)
    window_left.setSubSurfaceType("FixedWindow")

    window_right = op.model.SubSurface(window_vertices_right, model)
    window_right.setConstruction(window_construction)
    window_right.setName(surface.name().get() + " Window Right")
    window_right.setSurface(surface)
    window_right.setSubSurfaceType("FixedWindow")

    return window_left, window_right

# Definition to create a door sub-surface
'''
Description: This function creates a door sub-surface for a given surface with a given fraction of the building height, door width, U-factor, thickness and building height. The function returns a door sub-surface, which can be used to create a thermal zone.
Inputs:
    model: op.model.Model
    surface: op.model.Surface
    fraction_building_height: float in range [0, 1]
    door_width: float in m
    u_factor: float in W/m2K
    thickness: float in m
    building_height: float in m
Outputs:
    door_subsurface: op.model.SubSurface
'''
def create_door(model, surface, fraction_building_height, door_width, u_factor, thickness, building_height):
    # Define the door material to be opaque with a U-factor
    door_material = op.model.StandardOpaqueMaterial(model)
    door_material.setName("Door Material")
    door_material.setThickness(thickness)
    # Calculate the conductivity based on the U-factor
    conductivity = 1 / u_factor
    door_material.setConductivity(conductivity)

    # Define the door construction
    door_construction = op.model.Construction(model)
    door_construction.insertLayer(0, door_material)

    # Get the vertices of the surface
    surface_vertices = list(surface.vertices())

    # Place the door in the middle of the surface and at 0.01m above the ground (z = 0) and with the given height and width
    

    # Create the door sub-surface
    door_vertices = calculate_door_vertices(surface, fraction_building_height, door_width, 0.01, building_height)
    door_subsurface = op.model.SubSurface(door_vertices, model)
    door_subsurface.setConstruction(door_construction)
    door_subsurface.setName(surface.name().get() + " Door")
    door_subsurface.setSurface(surface)

    # Set the subsurface type to "Door"
    door_subsurface.setSubSurfaceType("Door")

    return door_subsurface