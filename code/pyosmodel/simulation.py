import os
import subprocess
# Definition of the function to run the simulation on idf files
'''
Description: This function runs the simulation and returns the results.
Inputs:
    - idf_relative_filepath: relative path to the idf file
    - epw_relative_filepath: relative path to the epw file
    - output_relative_directory: relative path to the output directory
    - energyplus_install_dir: relative path to the EnergyPlus installation directory
Outputs:
    - None
'''

def run_simulation(idf_relative_filepath, epw_relative_filepath, output_relative_directory, energyplus_install_dir): 
    # Create a folder for the outputs
    if not os.path.exists(output_relative_directory):
        os.mkdir(output_relative_directory)

    cl_st=(f'"{energyplus_install_dir}\\EnergyPlus" '
    + '--readvars '  # included to create a .csv file of the results
    + f'--output-directory "{output_relative_directory}" '
    + f'--weather "{epw_relative_filepath}" '
    + f'"{idf_relative_filepath}"'
    )
 
    result=subprocess.run(cl_st)

    try:
        subprocess.check_call(cl_st)
    except subprocess.CalledProcessError as e:
         raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    return None