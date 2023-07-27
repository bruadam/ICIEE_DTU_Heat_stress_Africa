import openstudio as op
from pyosmodel.schedule import set_schedule_always_on_off

## Heating Coil ##

# Definition to add a heating coil to a thermal zone
'''
Description: This function adds a heating coil to a given thermal zone with a given heating setpoint schedule. The function returns a heating coil instance, which can be used to create a thermal zone.
Input:
- model: op.model.Model
- thermal_zone: op.model.ThermalZone
- power: float in Watts
- heating_setpoint_schedule: op.model.Schedule
Output: heating_coil_instance: op.model.CoilHeatingElectric
'''
def add_coil_heater(model, thermal_zone, power, heating_setpoint_schedule):
    elec_heater = op.model.CoilHeatingElectric(model)
    elec_heater.setAvailabilitySchedule(set_schedule_always_on_off(model, True))
    elec_heater.setEfficiency(1)
    elec_heater.setNominalCapacity(power)
    elec_heater.setTemperatureSetpointNode(thermal_zone.zoneAirNode())

    return elec_heater

# Definition to add infiltration to a space
'''
Description: This function adds infiltration to a given space with a given design flow rate and schedule. The function returns an infiltration instance, which can be used to create a thermal zone.
Input: model, space, design_flow_rate, schedule
Output: infiltration_instance
'''
def add_infiltration(model, space, design_flow_rate_m3, schedule):
    infiltration = op.model.SpaceInfiltrationDesignFlowRate(model)
    infiltration.setName("Infiltration")
    infiltration.setSpace(space)
    infiltration.setSchedule(schedule)
    volume = space.volume()
    design_flow_rate = (design_flow_rate_m3 * volume) / 3600
    infiltration.setDesignFlowRate(design_flow_rate)

    return infiltration

# Definition to add a thermostat to a thermal zone
'''
Description: This function adds a thermostat to a given thermal zone with a given heating and cooling setpoint schedule. The function returns a thermostat instance, which can be used to create a thermal zone.
Input:
- model: op.model.Model
- thermal_zone: op.model.ThermalZone
- heating_setpoint_schedule: op.model.Schedule
Output: thermostat_instance: op.model.Thermostat
'''
def add_thermostat(model, thermal_zone, heating_setpoint_schedule):
    thermostat = op.model.Thermostat()
    thermostat.setName("Thermostat")
    thermostat.setHeatingSetpointTemperatureSchedule(heating_setpoint_schedule)
    # There is no cooling setpoint

    thermostat_instance = op.model.Thermostat(thermostat)
    thermostat_instance.setThermalZone(thermal_zone)

    return thermostat_instance