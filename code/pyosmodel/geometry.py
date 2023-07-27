import openstudio as op
from pyosmodel.utils import get_surface_normal_vector, calculate_center_point

# Definition to create a box geometry with a given length, width and height and add it to a given space in a given model
'''
Description: This function creates a box geometry with a given length, width and height and adds it to a given space in a given model
Inputs: model, space, length, width, height
Outputs: None
'''
def create_geometry_box(model, space, length, width, height):
    # Define points for the exterior walls
    wall_vertices1 = op.Point3dVector()
    wall_vertices1.push_back(op.Point3d(0, 0, 0))
    wall_vertices1.push_back(op.Point3d(0, 0, height))
    wall_vertices1.push_back(op.Point3d(0, width, height))
    wall_vertices1.push_back(op.Point3d(0, width, 0))

    wall_vertices2 = op.Point3dVector()
    wall_vertices2.push_back(op.Point3d(length, 0, 0))
    wall_vertices2.push_back(op.Point3d(length, width, 0))
    wall_vertices2.push_back(op.Point3d(length, width, height))
    wall_vertices2.push_back(op.Point3d(length, 0, height))

    wall_vertices3 = op.Point3dVector()
    wall_vertices3.push_back(op.Point3d(0, 0, 0))
    wall_vertices3.push_back(op.Point3d(length, 0, 0))
    wall_vertices3.push_back(op.Point3d(length, 0, height))
    wall_vertices3.push_back(op.Point3d(0, 0, height))

    wall_vertices4 = op.Point3dVector()
    wall_vertices4.push_back(op.Point3d(0, width, 0))
    wall_vertices4.push_back(op.Point3d(0, width, height))
    wall_vertices4.push_back(op.Point3d(length, width, height))
    wall_vertices4.push_back(op.Point3d(length, width, 0))

    walls = [wall_vertices1, wall_vertices2, wall_vertices3, wall_vertices4]

    for index, wall in enumerate(walls):
        surface = op.model.Surface(wall, model)
        surface.setSpace(space)
        surface.setOutsideBoundaryCondition("Outdoors")
        surface.setSurfaceType("Wall")
        surface.setName("Wall " + str(index+1))

    # Define points for the roof
    roof_vertices = op.Point3dVector()
    roof_vertices.push_back(op.Point3d(length, 0, height))
    roof_vertices.push_back(op.Point3d(length, width, height))
    roof_vertices.push_back(op.Point3d(0, width, height))
    roof_vertices.push_back(op.Point3d(0, 0, height))
    
    # Create the surface for the roof
    roof_surface = op.model.Surface(roof_vertices, model)
    roof_surface.setSpace(space)
    roof_surface.setOutsideBoundaryCondition("Outdoors")
    roof_surface.setSurfaceType("RoofCeiling")
    roof_surface.setName("Roof")

    # Define points for the floor
    floor_vertices = op.Point3dVector()
    floor_vertices.push_back(op.Point3d(0, 0, 0))
    floor_vertices.push_back(op.Point3d(0, width, 0))
    floor_vertices.push_back(op.Point3d(length, width, 0))
    floor_vertices.push_back(op.Point3d(length, 0, 0))

    # Create the surface for the floor
    floor_surface = op.model.Surface(floor_vertices, model)
    floor_surface.setSpace(space)
    floor_surface.setOutsideBoundaryCondition("Ground")
    floor_surface.setSurfaceType("Floor")
    floor_surface.setName("Floor")

    return model

# Define the window's vertices based on the center point, width and height
'''
Description: Creates a list of vertices for a window with a given center point, width and height
Inputs:
    center_point: op.Point3d
    width: float in meters
    height: float in meters
Outputs:
    window_vertices: list of op.Point3d
'''
def create_window_vertices(surface, center_point, width, height):

    half_width = width / 2
    half_height = height / 2
    normal_vector, unit_vector = get_surface_normal_vector(surface)
    # Define the vertices of the window depending on the surface normal vector
    if normal_vector.x() == 1:
        lower_left = op.Point3d(center_point.x(), center_point.y() - half_width, center_point.z() - half_height)
        lower_right = op.Point3d(center_point.x(), center_point.y() + half_width, center_point.z() - half_height)
        upper_right = op.Point3d(center_point.x(), center_point.y() + half_width, center_point.z() + half_height)
        upper_left = op.Point3d(center_point.x(), center_point.y() - half_width, center_point.z() + half_height)
    if normal_vector.x() == -1:
        lower_left = op.Point3d(center_point.x(), center_point.y() + half_width, center_point.z() - half_height)
        lower_right = op.Point3d(center_point.x(), center_point.y() - half_width, center_point.z() - half_height)
        upper_right = op.Point3d(center_point.x(), center_point.y() - half_width, center_point.z() + half_height)
        upper_left = op.Point3d(center_point.x(), center_point.y() + half_width, center_point.z() + half_height)
    if normal_vector.y() == -1:
        lower_left = op.Point3d(center_point.x() - half_width, center_point.y(), center_point.z() - half_height)
        lower_right = op.Point3d(center_point.x() + half_width, center_point.y(), center_point.z() - half_height)
        upper_right = op.Point3d(center_point.x() + half_width, center_point.y(), center_point.z() + half_height)
        upper_left = op.Point3d(center_point.x() - half_width, center_point.y(), center_point.z() + half_height)
    if normal_vector.y() == 1:
        lower_left = op.Point3d(center_point.x() + half_width, center_point.y(), center_point.z() - half_height)
        lower_right = op.Point3d(center_point.x() - half_width, center_point.y(), center_point.z() - half_height)
        upper_right = op.Point3d(center_point.x() - half_width, center_point.y(), center_point.z() + half_height)
        upper_left = op.Point3d(center_point.x() + half_width, center_point.y(), center_point.z() + half_height)
        
    if normal_vector.x() != 1 and normal_vector.x() != -1 and normal_vector.y() != 1 and normal_vector.y() != -1:
        raise ValueError("The surface normal vector is not aligned with the X or Y axis. Surface name = " + str(surface.name().get()) + ". Surface normal vector = " + str(normal_vector))

    window_vertices = [lower_left, lower_right, upper_right, upper_left]

    return window_vertices

# Defintion to calculate the vertices of a door based on a given surface, fraction of the building height, door width, height above ground and building height
'''
Description: This function calculates the vertices of a door based on a given surface, fraction of the building height, door width, height above ground and building height
Inputs:
    surface: op.model.Surface
    fraction_building_height: float in range [0, 1]
    door_width: float in meters
    height_above_ground: float in meters
    building_height: float in meters
Outputs:
    door_vertices: list of op.Point3d
'''
def calculate_door_vertices(surface, fraction_building_height, door_width, height_above_ground, building_height):
    # Get the normal vector of the surface
    normal_vector, unit_vector = get_surface_normal_vector(surface)

    # Calculate the center point of the surface
    center_point = calculate_center_point(surface)

    door_height = fraction_building_height * building_height

    # Calculate the half-width and half-height of the door
    half_width = door_width / 2
    if normal_vector.x() == 1:
        door_lower_left = op.Point3d(center_point.x(), center_point.y() - half_width, height_above_ground)
        door_lower_right = op.Point3d(center_point.x(), center_point.y() + half_width, height_above_ground)
        door_upper_right = op.Point3d(center_point.x(), center_point.y() + half_width, height_above_ground + door_height)
        door_upper_left = op.Point3d(center_point.x(), center_point.y() - half_width, height_above_ground + door_height)
    elif normal_vector.x() == -1:
        door_lower_left = op.Point3d(center_point.x(), center_point.y() + half_width, height_above_ground)
        door_lower_right = op.Point3d(center_point.x(), center_point.y() - half_width, height_above_ground)
        door_upper_right = op.Point3d(center_point.x(), center_point.y() - half_width, height_above_ground + door_height)
        door_upper_left = op.Point3d(center_point.x(), center_point.y() + half_width, height_above_ground + door_height)
    elif normal_vector.y() == -1:
        door_lower_left = op.Point3d(center_point.x() - half_width, center_point.y(), height_above_ground)
        door_lower_right = op.Point3d(center_point.x() + half_width, center_point.y(), height_above_ground)
        door_upper_right = op.Point3d(center_point.x() + half_width, center_point.y(), height_above_ground + door_height)
        door_upper_left = op.Point3d(center_point.x() - half_width, center_point.y(), height_above_ground + door_height)
    elif normal_vector.y() == 1:
        door_lower_left = op.Point3d(center_point.x() + half_width, center_point.y(), height_above_ground)
        door_lower_right = op.Point3d(center_point.x() - half_width, center_point.y(), height_above_ground)
        door_upper_right = op.Point3d(center_point.x() - half_width, center_point.y(), height_above_ground + door_height)
        door_upper_left = op.Point3d(center_point.x() + half_width, center_point.y(), height_above_ground + door_height)
    else:
        raise ValueError("The surface normal vector is not aligned with the X or Y axis. Surface name: " + str(surface.name().get()) + ". Normal vector: " + str(normal_vector))
        
    door_vertices = [door_lower_left, door_lower_right, door_upper_right, door_upper_left]
    return door_vertices