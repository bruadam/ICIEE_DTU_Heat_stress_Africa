import openstudio as op

# Set up simulation controls
'''
Description: This function sets up the simulation controls with a given simulation start and end date. The function returns a simulation control and run period instance, which can be used to create a model.
Input:
- model: op.model.Model
- simulation_start: datetime
- simulation_end: datetime
Output: simulation_control, run_period
'''
def setup_simulation_control(model, simulation_start, simulation_end):
    # Set the simulation control
    simulation_control = model.getSimulationControl()
    simulation_control.setRunSimulationforSizingPeriods(False)
    simulation_control.setRunSimulationforWeatherFileRunPeriods(True)
    
    
    # Set the simulation period
    run_period = model.getRunPeriod()
    run_period.setBeginMonth(simulation_start.month)
    run_period.setBeginDayOfMonth(simulation_start.day)
    run_period.setEndMonth(simulation_end.month)
    run_period.setEndDayOfMonth(simulation_end.day)

    return simulation_control, run_period

# Definition to change the timestep of the simulation
'''
Description: This function changes the timestep of the simulation. The function returns a model with the new timestep.
Input:
- model: op.model.Model
- timestep: int
Output: model
'''
def change_timestep(model, step):
    timestep = model.getTimestep()
    timestep.setNumberOfTimestepsPerHour(step)
    return model