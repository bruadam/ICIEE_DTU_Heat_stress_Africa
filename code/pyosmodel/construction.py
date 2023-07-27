import openstudio as op

# Defintion of a material list from a imported material database
'''
Description: This function creates a list of materials from a given material database. The material database is a list of lists, where each list contains the following information about a material: name, thickness, conductivity, density, specific heat, thermal absorptance and solar absorptance. The function returns a list of materials, which can be used to create a construction.
Input: model, material_database
Output: material_list
'''
def create_material_list(model, material_database):
    material_list = []
    for material in material_database:
        material_name = material[0]
        material_thickness = material[1]
        material_conductivity = material[2]
        material_density = material[3]
        material_specific_heat = material[4]
        material_thermal_absorptance = material[5]
        material_solar_absorptance = material[6]
        
        material = op.model.StandardOpaqueMaterial(model)
        material.setName(material_name)
        material.setThickness(material_thickness)
        material.setConductivity(material_conductivity)
        material.setDensity(material_density)
        material.setSpecificHeat(material_specific_heat)
        material.setThermalAbsorptance(material_thermal_absorptance)
        material.setSolarAbsorptance(material_solar_absorptance)

        
        material_list.append(material)
        
    return material_list

# Definition to create a construction from a given set of material layers
'''
Description: This function creates a construction with a given set of material layers. The function returns a construction, which can be used to create a surface.
Input: model, name, materials layers
Output: construction
'''
def create_construction(model, name, materials):
    construction = op.model.Construction(model)
    construction.setName(name)
    # Add material layers from materials list
    for index, material in enumerate(materials):
        construction.insertLayer(index, material)

    return construction

# Defintion to assign a construction to a surface
'''
Description: This function assigns a construction to a given surface.
Input: surface, construction
Output: None
'''
def assign_construction(surface, construction):
    surface.setConstruction(construction)

# Define the window construction
'''
Description: Creates a window construction with a given u-factor and shgc
Inputs:
    model: op.model.Model
    u_factor: float
    shgc: float
Outputs:
    window_construction: op.model.Construction
'''
def create_window_construction(model, u_factor, shgc):
    window_material = op.model.SimpleGlazing(model)
    window_material.setUFactor(u_factor)
    window_material.setSolarHeatGainCoefficient(shgc)

    window_construction = op.model.Construction(model)
    window_construction.insertLayer(0, window_material)
    
    return window_construction