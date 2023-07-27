import openstudio as op

# Set up the output variables
'''
Description: This function sets up the output variables. The function returns a model with the output variables.
Output variables : output_data
Input:
- model: op.model.Model
Output: model
'''
def set_output_variables(model, output_data):
    # Create an OutputVariable object for each desired variable listed in output_data

    output_variables = []
    for item in output_data:
        output_variable = {
            'variableName': item,
            'keyValue': '*',
            'reportingFrequency': 'Timestep',
            'exportToBCVTB': False
        }
        output_variables.append(output_variable)

    # Add the output variables to the model
    for output_variable in output_variables:
        variable_name = output_variable['variableName']
        key_value = output_variable['keyValue']
        reporting_frequency = output_variable['reportingFrequency']
        export_to_bcvtb = output_variable['exportToBCVTB']

        output_variable_object = op.model.OutputVariable(variable_name, model)
        output_variable_object.setKeyValue(key_value)
        output_variable_object.setReportingFrequency(reporting_frequency)
        output_variable_object.setExportToBCVTB(export_to_bcvtb)

    return model