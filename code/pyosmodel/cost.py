import openstudio as op

# Definition of the function to add life cycle costs to the model
'''
Description: This function adds life cycle costs to the model. The function returns a life cycle costs object, which can be used to add life cycle costs to different components.
Inputs:
    - model: op.model.Model
    - construction_cost: float
    - electricity_cost: float
    - natural_gas_cost: float
Outputs:
    - lifecycle_costs: op.model.LifeCycleCosts
'''
def add_lcc(model, construction_cost, electricity_cost, natural_gas_cost):
    # Get the life cycle costs object
    lifecycle_costs = model.getLifeCycleCosts()

    # Set up the currency for the costs
    currency = op.CurrencyType('DKK')  # Specify the currency as Danish Krone
    lifecycle_costs.setCurrency(currency)

    # Create life cycle cost objects for different components
    construction_cost = 100000  # Example construction cost in DKK
    construction_lcc = lifecycle_costs.addLifeCycleCost('Construction', construction_cost)

    # Set up energy cost resources and escalation rates
    electricity_resource = model.getElectricityResource()
    electricity_lcc = lifecycle_costs.addLifeCycleCost('Electricity', 0)  # Set initial cost to 0
    electricity_lcc.setCostUnits('kWh')  # Set the cost units to kilowatt-hours
    electricity_lcc.setUsePriceEscalation('Electricity', electricity_resource)

    natural_gas_resource = model.getNaturalGasResource()
    natural_gas_lcc = lifecycle_costs.addLifeCycleCost('NaturalGas', 0)  # Set initial cost to 0
    natural_gas_lcc.setCostUnits('Therms')  # Set the cost units to therms
    natural_gas_lcc.setUsePriceEscalation('NaturalGas', natural_gas_resource)

    # Apply the life cycle costs to the model 
    lifecycle_costs.applyCosts()
    return lifecycle_costs