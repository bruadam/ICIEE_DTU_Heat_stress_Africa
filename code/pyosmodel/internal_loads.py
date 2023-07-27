import openstudio as op
# Definition to add people to a given space with a given schedule and people per area and fraction radiant
'''
Description: This function adds people to a given space with a given schedule and people per area and fraction radiant. The function returns a people instance, which can be used to create a thermal zone.
Input: model, space, people_per_area, fraction_radiant, people_schedule
Output: people_instance
'''
def add_people(model, space, people_per_area, fraction_radiant, people_schedule, people_activity_schedule):
    people = op.model.PeopleDefinition(model)
    people.setName("People")
    people.setPeopleperSpaceFloorArea(people_per_area)
    people.setSpaceFloorAreaperPerson(1/people_per_area)
    people.setFractionRadiant(fraction_radiant)
    people.setSensibleHeatFraction(0.5)
    people.setCarbonDioxideGenerationRate(0.0117) # 0.0117 m3/s/person : 42,12 l/h/person
    people.setEnableASHRAE55ComfortWarnings(False)
    people.setMeanRadiantTemperatureCalculationType("ZoneAveraged")
    
    people_instance = op.model.People(people)
    people_instance.setSpace(space)
    people_instance.setNumberofPeopleSchedule(people_schedule)
    people_instance.setActivityLevelSchedule(people_activity_schedule)
    
    return people_instance

# Definition to add lighting to a space
'''
Description: This function adds lighting to a given space with a given lighting per area and schedule. The function returns a lighting instance, which can be used to create a thermal zone.
Input: model, space, lighting_per_area, schedule
Output: lighting_instance
'''
def add_lighting(model, space, lighting_per_area, schedule):
    lighting = op.model.LightsDefinition(model)
    lighting.setName("Lights")
    lighting.setWattsperSpaceFloorArea(lighting_per_area)
    lighting.setFractionRadiant(0.1) # Incandescent lights bulbs
    lighting.setFractionVisible(0.9) # Good Assumption for lighting

    lighting_instance = op.model.Lights(lighting)
    lighting_instance.setSpace(space)
    lighting_instance.setSchedule(schedule)

    return lighting_instance

# Definition to add electric equipment to a space
'''
Description: This function adds electric equipment to a given space with a given electric equipment per area and schedule. The function returns an electric equipment instance, which can be used to create a thermal zone.
Input: 
- model: op.model.Model
- space: op.model.Space
- electric_equipment_per_area: float in W/m2
- schedule: op.model.Schedule
Output: electric_equipment_instance: op.model.ElectricEquipment
'''
def add_electric_equipment(model, space, electric_equipment_per_area, schedule):
    electric_equipment_def = op.model.ElectricEquipmentDefinition(model)
    electric_equipment_def.setName("Electric Equipment")
    electric_equipment_def.setWattsperSpaceFloorArea(electric_equipment_per_area)
    electric_equipment_def.setFractionRadiant(0.5) # Assumptions for electric stoves
    electric_equipment_def.setFractionLatent(0.4) # Assumption for boiling water => conservative because moisture is critical in the model
    electric_equipment_def.setFractionLost(0.1) # Assumption for poor quality electric equipment
    
    electric_equipment = op.model.ElectricEquipment(electric_equipment_def)
    electric_equipment.setSpace(space)
    electric_equipment.setSchedule(schedule)

    return electric_equipment

# Definition to add gas equipment to a space
'''
Description: This function adds gas equipment to a given space with a given gas equipment per area and schedule. The function returns a gas equipment instance, which can be used to create a thermal zone.
Input:
- model: op.model.Model
- space: op.model.Space
- gas_equipment_per_area: float in W/m2
- schedule: op.model.Schedule
Output: gas_equipment_instance: op.model.GasEquipment
'''
def add_gas_equipment(model, space, gas_equipment_per_area, schedule):
    gas_equipment = op.model.GasEquipmentDefinition(model)
    gas_equipment.setName("Gas Equipment")
    gas_equipment.setWattsperSpaceFloorArea(gas_equipment_per_area)
    gas_equipment.setFractionRadiant(0.5) # Assumptions for gas stoves
    gas_equipment.setFractionLatent(0.3) # Conservative value
    gas_equipment.setFractionLost(0.2) # Assumption for poor quality gas equipment

    gas_equipment_instance = op.model.GasEquipment(gas_equipment)
    gas_equipment_instance.setSpace(space)
    gas_equipment_instance.setSchedule(schedule)

    return gas_equipment_instance

