import openstudio as op
from datetime import datetime, timedelta
import pandas as pd
from pyosmodel.utils import convert_hour_to_datetime, get_op_time, get_start_end_time


# Set the occupancy schedule
'''
Description: This function creates a schedule for the occupancy of the building. The schedule is based on the following assumptions:
    - The building is occupied from 6 AM to 6 PM on weekdays
    - The building is occupied from 0 AM to 12 AM on weekends
    - The building is unoccupied at all other times
'''
def set_occupancy_schedule(model):
    default_schedule_type_limits = op.model.ScheduleTypeLimits(model)
    default_schedule_type_limits.setLowerLimitValue(0)
    default_schedule_type_limits.setUpperLimitValue(1)
    default_schedule_type_limits.setNumericType("Discrete")
    default_schedule_type_limits.setUnitType("Dimensionless")
    default_schedule_type_limits.setName("Occupancy Fraction Schedule Type Limits")

    occupancy_schedule = op.model.ScheduleRuleset(model)
    occupancy_schedule.setName("Occupancy Fraction Schedule")
    occupancy_schedule.setScheduleTypeLimits(default_schedule_type_limits)

    # Create a rule for the default schedule (1 = occupied, 0 = unoccupied) 
    # 0 - 6 AM occupied
    # 6 AM - 6 PM unoccupied
    # 6 PM - 12 AM occupied
    default_day = occupancy_schedule.defaultDaySchedule()
    default_day.addValue(op.Time(0, 0, 0, 0), 0)
    default_day.addValue(op.Time(0, 6, 0, 0), 1)
    default_day.addValue(op.Time(0, 18, 0, 0), 0)
    default_day.addValue(op.Time(0, 24, 0, 0), 1)

    # Create a rule for the weekend schedule (1 = occupied, 0 = unoccupied)
    # occupied all day
    weekend_rule = op.model.ScheduleRule(occupancy_schedule)
    weekend_rule.setName("Weekend")
    weekend_rule.setApplySaturday(True)
    weekend_rule.setApplySunday(True)

    weekend_day = weekend_rule.daySchedule()
    weekend_day.addValue(op.Time(0, 0, 0, 0), 1)
    weekend_day.addValue(op.Time(0, 24, 0, 0), 1)

    return occupancy_schedule

# Set the lighting schedule
'''
Description: This function creates a schedule for the lighting of the building. The schedule is based on the following assumptions:
    - The building is lit from 6 AM to 6 PM on weekdays
    - The building is lit from 0 AM to 12 AM on weekends
    - The building is unlit at all other times
'''
# def set_lighting_scheduleYear(model, csv_path):
#     # Import csv file
#     file = pd.read_csv(csv_path, header=0)
    
#     # Convert the time column (which is an hour from 0 to 8759) to a datetime object
#     for hour in file['Hour']:
#         converted_hour = convert_hour_to_datetime(hour, year=2023, month=1, day=1)
#         file['Hour'][hour] = converted_hour
    
#     # Get start and end date
#     start_date = file['Hour'][0]
#     end_date = file['Hour'][len(file['Hour'])-1]
        
    
#     schedule_rule_year = op.model.ScheduleYear(model)
#     schedule_rule_year.setName("Lighting Schedule Rule Year")

#     schedule_day = op.model.ScheduleDay(start_date, schedule_rule_year)

#     # Iterate over each day in the file and add the lighting schedule
#     for _, row in file.iterrows():
#         hour = row['Hour']
#         sunhours = row['Sunhours']

#         # Extract the hour, minute and second from the datetime object
#         day = hour.timetuple().tm_yday
#         hour = hour.hour
#         minute = hour.minute
#         second = hour.second

#         # Create a time object for the current hour
#         time = op.Time(day, hour, minute, second)

#         # Add the sunhours to the schedule
#         schedule_day.addValue(time, sunhours)
    
#     # Add the schedule to the schedule rule year
#     schedule_rule_year.setSchedule(schedule_day)

#     # Create a schedule rule set
#     lighting_schedule = op.model.ScheduleRuleset(model)
#     lighting_schedule.setName("Lighting Schedule")
#     lighting_schedule.addRule(schedule_rule_year)

#     return lighting_schedule

# Definition of a lighting schedule
'''
Description: This function creates a schedule for the lighting of the building. The schedule is based on the following assumptions:
    - The building is lit from 4 AM to 6 AM
    - The building is lit from 6 PM to 10 PM
    - The building is unlit at all other times
Input:
    - model: op.model.Model 
Output:
    - lighting_schedule: op.model.Schedule
'''
def set_lighting_schedule(model):
    default_schedule_type_limits = op.model.ScheduleTypeLimits(model)
    default_schedule_type_limits.setLowerLimitValue(0)
    default_schedule_type_limits.setUpperLimitValue(1)
    default_schedule_type_limits.setNumericType("Discrete")
    default_schedule_type_limits.setUnitType("Dimensionless")
    default_schedule_type_limits.setName("Lighting Fraction Schedule Type Limits")

    lighting_schedule = op.model.ScheduleRuleset(model)
    lighting_schedule.setName("Lighting Fraction Schedule")
    lighting_schedule.setScheduleTypeLimits(default_schedule_type_limits)

    # Create a rule for the default schedule (1 = lit, 0 = unlit) 
    default_day = lighting_schedule.defaultDaySchedule()
    default_day.addValue(op.Time(0, 0, 0, 0), 0)
    default_day.addValue(op.Time(0, 4, 0, 0), 0)
    default_day.addValue(op.Time(0, 6, 0, 0), 1)
    default_day.addValue(op.Time(0, 18, 0, 0), 0)
    default_day.addValue(op.Time(0, 22, 0, 0), 1)
    default_day.addValue(op.Time(0, 24, 0, 0), 0)

    return lighting_schedule



# Set the equipment schedule
'''
Description: This function creates a schedule for the equipment of the building. The schedule is based on the following assumptions:
    - The equipment is used every day once from a specific start_time during a specific duration
Inputs: 
    - model: the model to which the schedule is added
    - start_time: the time at which the equipment is turned on as a datetime.time object
    - duration: the duration for which the equipment is turned on as a datetime.timedelta object
'''
def set_equipment_schedule(model, start_time, duration):
    # Set the equipment to be on at a specific time for a specific duration
    start_time, end_time = get_start_end_time(start_time, duration)
    start_time = get_op_time(start_time)
    end_time = get_op_time(end_time)

    equipment_schedule_type_limits = op.model.ScheduleTypeLimits(model)
    equipment_schedule_type_limits.setLowerLimitValue(0)
    equipment_schedule_type_limits.setUpperLimitValue(1)
    equipment_schedule_type_limits.setNumericType("Discrete")
    equipment_schedule_type_limits.setUnitType("Dimensionless")
    equipment_schedule_type_limits.setName("Equipment Schedule Type Limits")
    
    equipment_schedule = op.model.ScheduleRuleset(model)
    equipment_schedule.setName("Equipment Schedule")
    equipment_schedule.defaultDaySchedule().setName("Equipment Schedule Default")
    equipment_schedule.defaultDaySchedule().addValue(op.Time(0, 0, 0, 0), 0)
    equipment_schedule.defaultDaySchedule().addValue(start_time, 0)
    equipment_schedule.defaultDaySchedule().addValue(end_time, 1)
    equipment_schedule.defaultDaySchedule().addValue(op.Time(0, 24, 0, 0), 0)
    equipment_schedule.setScheduleTypeLimits(equipment_schedule_type_limits)
    return equipment_schedule

# Definition to set the heating set point schedule
'''
Description: This function creates a schedule for the heating set point of the building. The schedule is based on the following assumptions:
    - The heating set point is 15 degrees Celsius at all times
'''
def set_heating_set_point_schedule(model, heating_set_point):
    # Set schedule type limits
    schedule_type_limits = op.model.ScheduleTypeLimits(model)
    schedule_type_limits.setName("Heating Set Point Schedule Type Limits")
    schedule_type_limits.setLowerLimitValue(0)
    schedule_type_limits.setUpperLimitValue(100)
    schedule_type_limits.setNumericType("Continuous")
    schedule_type_limits.setUnitType("Temperature")

    # Set the heating set point to 15 degrees Celsius
    heating_set_point_schedule = op.model.ScheduleRuleset(model)
    heating_set_point_schedule.setName("Heating Set Point Schedule")
    heating_set_point_schedule.defaultDaySchedule().setName("Heating Set Point Schedule Default")
    heating_set_point_schedule.defaultDaySchedule().addValue(op.Time(0, 0, 0, 0), heating_set_point)
    heating_set_point_schedule.defaultDaySchedule().addValue(op.Time(0, 24, 0, 0), heating_set_point)
    return heating_set_point_schedule

def set_activity_level_schedule(model, activity_level):
    activity_level_schedule = op.model.ScheduleRuleset(model)
    activity_level_schedule.setName("Activity Level Schedule")
    activity_level_schedule.defaultDaySchedule().setName("Activity Level Schedule Default")
    activity_level_schedule.defaultDaySchedule().addValue(op.Time(0, 0, 0, 0), activity_level)
    activity_level_schedule.defaultDaySchedule().addValue(op.Time(0, 24, 0, 0), activity_level)
    return activity_level_schedule

def set_schedule_always_on_off(model, boolean):
    schedule_type_limits = op.model.ScheduleTypeLimits(model)
    schedule_type_limits.setName("Always On/Off Schedule Type Limits")
    schedule_type_limits.setLowerLimitValue(0)
    schedule_type_limits.setUpperLimitValue(1)
    schedule_type_limits.setNumericType("Discrete")
    schedule_type_limits.setUnitType("Dimensionless")

    if boolean == True:
        schedule = op.model.ScheduleRuleset(model)
        schedule.setName("Always On Schedule")
        schedule.defaultDaySchedule().setName("Always On Schedule Default")
        schedule.defaultDaySchedule().addValue(op.Time(0, 0, 0, 0), 1)
        schedule.defaultDaySchedule().addValue(op.Time(0, 24, 0, 0), 1)
        schedule.setScheduleTypeLimits(schedule_type_limits)
    else:
        schedule = op.model.ScheduleRuleset(model)
        schedule.setName("Always Off Schedule")
        schedule.defaultDaySchedule().setName("Always Off Schedule Default")
        schedule.defaultDaySchedule().addValue(op.Time(0, 0, 0, 0), 0)
        schedule.defaultDaySchedule().addValue(op.Time(0, 24, 0, 0), 0)
        schedule.setScheduleTypeLimits(schedule_type_limits)
    
    return schedule