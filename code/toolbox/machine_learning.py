#%% Import libraries
import numpy as np
import pandas as pd
import json
from sklearn.preprocessing import LabelEncoder
from pythermalcomfort.models import at, heat_index
from sklearn.preprocessing import StandardScaler

#%% Define functions
# Function to get the features sets
'''
Description: This function returns the features sets to be used in the machine learning models.
Inputs: selector (str): Selector to choose the features sets
Outputs: features (list): List of features sets

'''
def get_features_sets(selector):
    # Import features subset from features_subsets.json
    with open('features_subsets.json') as json_file:
        features_subsets = json.load(json_file)
    sets_detailed = {"Detailed": ['weather', 'building_geometry', 'building_construction_complex', 'building_envelope', 'occupancy_detailed', 'equipment', 'hvac', 'lighting', 'infiltration', 'day_period', 'history_temperature'], "Reduced": ['weather', 'building_geometry', 'building_construction_simple', 'building_envelope', 'occupancy_simple', 'equipment', 'hvac', 'day_period', 'history_temperature'], "Aggregated": ['weather', 'building_geometry', 'building_construction_simple', 'occupancy_simple', 'day_period', 'history_temperature'], "Highly-Aggregated": ['weather', 'type_house', 'day_period', 'history_temperature'], "all" : ['all']}
    # Get all the features from features_subsets.json according to the sets
    features = {}
    for key in sets_detailed.keys():
        features[key] = []
        for subset in sets_detailed[key]:
            features[key].extend(features_subsets[subset])

    return features[selector]

# Function to get the data for the machine learning models
'''
Description: This function returns the data for the machine learning models.
Inputs: scenario (str): Scenario to choose the data
        features (list): List of features
        target (str): Target variable
        scaler (bool): Whether to scale the data or not
Outputs: data (DataFrame): DataFrame with the data
'''
def get_data(scenario, features, target, scaler=False, periods=[]):
    data_path = '../results/simulations/' + scenario + '_simulation_data.csv'
    simulation_data = pd.read_csv(data_path)
    input_path = '../results/simulations/' + scenario + '_inputs.csv'
    input_data = pd.read_csv(input_path)

    # Merge data and inputs given key and index
    data = pd.merge(simulation_data, input_data, on=['key', 'key'])
    
    # Filter data on Datetime and keep year 2023
    data['Datetime'] = pd.to_datetime(data['Datetime'])
    data = data[data['Datetime'].dt.year == 2023]
    # Filter data on Datetime and keep the periods of interest stored in period under the form of a list of two datetime objects [start, end]
    if periods != []:
        filtered_data = pd.DataFrame()
        for period in periods: # Assuming periods is your list of periods
            start_date = pd.to_datetime(period[0])
            end_date = pd.to_datetime(period[1])
            period_data = data[(data['Datetime'] >= start_date) & (data['Datetime'] <= end_date)]
            filtered_data = pd.concat([filtered_data, period_data])
        data = filtered_data
    
    data['apparent_temperature'] = data.apply(lambda row: at(tdb=row['Indoor Mean Air Temperature'], rh=row['Indoor Air Relative Humidity'], v=0, q=0), axis=1)
    
    data['history_temperature'] = data.groupby('key')['Outdoor Dry Bulb Temperature'].rolling(6).mean().reset_index(0, drop=True)
    
    data['day_period'] = data['Datetime'].dt.hour.apply(lambda x: 'morning' if x >= 6 and x < 12 else ('afternoon' if x >= 12 and x < 18 else ('evening' if x >= 18 and x < 22 else 'night')))
    
    data['heat_stress_category'] = data['apparent_temperature'].apply(lambda x: 4 if x >= 54 else (3 if x >= 40 and x < 54 else (2 if x >= 32 and x < 40 else ( 1 if x >= 27 and x < 32 else 0))))

    # Group values in data['Wind Direction'] into 8 categories N, NE, E, SE, S, SW, W, NW
    data['Wind Direction'] = data['Wind Direction'].apply(lambda x: 'N' if x >= 337.5 or x < 22.5 else ('NE' if x >= 22.5 and x < 67.5 else ('E' if x >= 67.5 and x < 112.5 else ('SE' if x >= 112.5 and x < 157.5 else ('S' if x >= 157.5 and x < 202.5 else ('SW' if x >= 202.5 and x < 247.5 else ('W' if x >= 247.5 and x < 292.5 else 'NW')))))))

    # Encode categorical features
    le = LabelEncoder()

    categorical_features = ['day_period', 'type_house', 'elec_gas', 'heat_stress_category', 'Wind Direction', 'construction_type', 'orientation', 'Wind Direction', 'ceiling_insulation', 'wall_U_value', 'roof_U_value', 'ground_U_value']
    exception_features = ['heat_stress_category']
    for feature in categorical_features:
        if feature not in exception_features:
             data[feature] = le.fit_transform(data[feature])
             # save the encoder in a json file
             encoder_path = '../results/models/' + scenario + '_' + feature + '_encoder.json'
             with open(encoder_path, 'w') as f:
                 json.dump(dict(zip(le.classes_.tolist(), le.transform(le.classes_).tolist())), f)


    # Scale features that are not categorical
    scaling_features = [feature for feature in features if feature not in categorical_features]

    if scaler:
        scaler = StandardScaler()
        data[scaling_features] = scaler.fit_transform(data[scaling_features])
    
    data.dropna(inplace=True)

    return data[features], data[target]


# Function to balance the data
'''
Description: This function returns the balanced data.
Inputs: X (DataFrame): DataFrame with the features
        y (Series): Series with the target variable
Outputs: X (DataFrame): DataFrame with the features
            y (Series): Series with the target variable
'''
def balance_data(X, y):
    from sklearn.utils import resample
    min_class_size = y.value_counts().min()
    # Create balanced dataset
    df_balanced = pd.concat([X, y], axis=1)

    # Join X and y to create a balanced dataset
    df = pd.concat([X, y], axis=1)

    for class_ in y.unique():
        class_samples = df[df['heat_stress_category'] == class_]
        class_samples_downsampled = resample(class_samples, replace=False, n_samples=min_class_size, random_state=42)
        df_balanced = pd.concat([df_balanced, class_samples_downsampled])

    X = df_balanced.drop('heat_stress_category', axis=1)
    y = df_balanced['heat_stress_category']

    return X, y