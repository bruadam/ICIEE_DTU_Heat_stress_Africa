
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import numpy as np
import pandas as pd
from toolbox.figures import set_matplotlib_style, set_dtu_colors
import json
import os
import seaborn as sns
from toolbox.machine_learning import get_features_sets, get_data
set_matplotlib_style()
dtu_colors = set_dtu_colors()


#%% Models Comparative Analysis
# Load data
models = pd.read_csv('results/models/ml_comparative_analysis.csv')

# Order the models by accuracy
models = models.sort_values(by=['Accuracy'], ascending=False)
# Plot the results
fig, ax1 = plt.subplots(figsize=(10, 6))
ax2 = ax1.twinx()

bar_width = 0.4

ax1.bar(models['Model'], models['Accuracy'], color=dtu_colors['dtu_blue'], width=-bar_width, align='edge')
ax2.bar(models['Model'], models['Time Taken'], color=dtu_colors['dtu_green'], width=bar_width, align='edge', alpha=0.3)
ax1.hlines(0.6, -1, 10, colors=dtu_colors['dtu_red'], linestyles='dashed', label='Selection Threshold')

ax1.set_ylabel('Models Accuracy * 100 [%]')
ax1.set_ylim([0, 1])
ax1.set_xticklabels(models['Model'], rotation=90)
ax1.grid(True)
ax1.xaxis.grid(False)

ax2.set_ylabel('Models training duration [s]')
ax2.set_yscale('log')
ax2.set_yticks(np.logspace(0, 4, 5))
ax2.grid(False)

# Create legend handles and labels
blue_bar = mpatches.Patch(color=dtu_colors['dtu_blue'], label='Accuracy')
green_bar = mpatches.Patch(color=dtu_colors['dtu_green'], label='Model training duration', alpha=0.3)
red_line = mlines.Line2D([], [], color=dtu_colors['dtu_red'], linestyle='dashed', label='Selection Threshold')

# Create a single legend for all handles and labels
handles = [blue_bar, green_bar, red_line]
labels = [handle.get_label() for handle in handles]
ax1.legend(handles=handles, labels=labels, loc='upper right')

# ax1.set_title('Models Accuracy and respective Computing time')
plt.tight_layout()
plt.savefig('figures/machine_learning/ml_comparative_analysis.png', dpi=300)
plt.show()


#%% Plot for 4 features sets the accuracy, duration
# Load data from json files in results/features/
files = os.listdir('results/features/')
files = [file for file in files if file.endswith('.json')]

# Get the sets names
sets = [file.split('.')[0] for file in files]
sets = [set.split('_')[-1] for set in sets]

# Load the data from the json files
accuracies = []
durations = []
for file in files:
    with open('results/features/' + file) as f:
        data = json.load(f)
    accuracies.append(data['accuracy'])
    durations.append(data['duration'])

# Order to have th detailed than medium than simple than elementary
sets = [sets[1], sets[3], sets[0], sets[2]]
accuracies = [accuracies[1], accuracies[3], accuracies[0], accuracies[2]]
durations = [durations[1], durations[3], durations[0], durations[2]]

# Plot the results
fig, ax1 = plt.subplots(figsize=(10, 6))
ax2 = ax1.twinx()

bar_width = 0.3
ax1.bar(sets, accuracies, color=dtu_colors['dtu_blue'], width=-bar_width, align='edge')
ax2.bar(sets, durations, color=dtu_colors['dtu_green'], width=bar_width, align='edge', alpha=0.3)


ax1.set_ylabel('Models Accuracy * 100 [%]')
ax1.set_ylim([0, 1])
ax1.set_xticklabels(sets, rotation=90)
ax1.grid(True)
ax1.xaxis.grid(False)

ax2.set_ylabel('Models training duration [s]')
ax2.set_yscale('log')
ax2.set_yticks(np.logspace(0, 4, 5))
ax2.grid(False)

# Create legend handles and labels
blue_bar = mpatches.Patch(color=dtu_colors['dtu_blue'], label='Accuracy')
green_bar = mpatches.Patch(color=dtu_colors['dtu_green'], label='Model training duration', alpha=0.3)

# Create a single legend for all handles and labels
handles = [blue_bar, green_bar]
labels = [handle.get_label() for handle in handles]
ax1.legend(handles=handles, labels=labels, loc='upper right')
# tight_layout
plt.tight_layout()
# ax1.set_title('Accuracy and Duration for each features set')
plt.savefig('figures/features_selection/features_sets_accuracy_duration.png', dpi=300)
plt.show()



#%% Plot the feature importance for the different models in 4 subplots
# Load data
files = os.listdir('results/features/')
files = [file for file in files if file.startswith('feature_importances_')]

# Get the sets names
sets = [file.split('.')[0] for file in files]
sets = [set.split('_')[-1] for set in sets]

# Load the data from the csv files
feature_importances = {}
for i, file in enumerate(files):
    feature_importances[sets[i]] = pd.read_csv('results/features/' + file)

for item in sets:
    feature_importances[item] = feature_importances[item].set_index('Unnamed: 0')

# Order the sets
sets = [sets[1], sets[3], sets[0], sets[2]]

# Plot the results
fig, axs = plt.subplots(2, 2, figsize=(16, 16))
axs = axs.ravel()

for i, item in enumerate(sets):
    feature_importances[item].plot.bar(ax=axs[i], legend=False, color=dtu_colors['dtu_blue'])
    # Plot a dashed line at 0.01 over all the bars (based on length of the dataframe)
    axs[i].hlines(0.01, -1, len(feature_importances[item]), colors=dtu_colors['dtu_red'], linestyles='dashed', label='Selection Threshold')
    axs[i].set_title(item)
    axs[i].set_ylabel('Feature importance')
    axs[i].set_xlabel('Features')
    axs[i].grid(True)
    axs[i].xaxis.grid(False)
    axs[i].set_xticklabels(feature_importances[item].index, rotation=90)
    

# Give more space between the subplots
fig.subplots_adjust(hspace=0.7, wspace=0.2)
# fig.suptitle('Feature importance for each features set')
plt.savefig('figures/features_selection/features_sets_feature_importance.png', dpi=300)
plt.show()



#%% Import simulation Data

period = [['2023-01-01 00:00:00', '2023-12-31 23:00:00']]
scenarios = ['present-day', '2050', '2080']
df  = {}
for scenario in scenarios:
    # Import the data
    features = ['Datetime', 'Outdoor Dry Bulb Temperature', 'Outdoor Relative Humidity', 'Indoor Mean Air Temperature', 'Indoor Air Relative Humidity']
    df[scenario], y = get_data(scenario=scenario, features=features, periods=period, scaler=False, target='type_house')
    df[scenario] = pd.concat([df[scenario], y], axis=1)


for scenario in scenarios:
    # Densities histograms for Indoor Mean Air Temperature and Indoor Air Relative Humidity using Seaborn
    df[scenario]['Datetime'] = pd.to_datetime(df[scenario]['Datetime'])
    df[scenario]['month'] = df[scenario]['Datetime'].dt.month
    df[scenario]['hour'] = df[scenario]['Datetime'].dt.hour


# Group by month and type_house
df_grouped = {}
for scenario in scenarios:
    df_grouped[scenario] = df[scenario].groupby(['month', 'type_house']).mean()
    df_grouped[scenario] = df_grouped[scenario].reset_index()


# Plot the results
fig, axs = plt.subplots(1, 3, figsize=(16, 4))
axs = axs.ravel()

for i, scenario in enumerate(scenarios):
    # Replace 0 by RDP house and 1 by Shack house
    df_grouped[scenario]['type_house'] = df_grouped[scenario]['type_house'].replace(0, 'RDP')
    df_grouped[scenario]['type_house'] = df_grouped[scenario]['type_house'].replace(1, 'Shack')
    sns.lineplot(data=df_grouped[scenario], x='month', y='Indoor Mean Air Temperature', hue='type_house', ax=axs[i])
    axs[i].set_title(scenario)
    axs[i].set_ylabel('Monthly Mean Indoor Temperature [°C]')
    axs[i].set_xlabel('Month')
    axs[i].grid(True)
    axs[i].xaxis.grid(False)
    axs[i].set_ylim([18, 36])
    axs[i].set_xticks(np.arange(1, 13))
    axs[i].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct','Nov', 'Dec'])
    axs[i].legend(loc='best')
# Save the figure
plt.savefig('figures/simulations/indoor_mean_air_temperature_3 scenarios.png', dpi=300)
plt.show()


# Plot diurnal cycle for each month and each scenario

# Create a dataframe with the diurnal cycle for each month and each scenario
df_diurnal = {}
for scenario in scenarios:
    df_diurnal[scenario] = df[scenario].groupby(['month', 'hour']).mean()
    df_diurnal[scenario] = df_diurnal[scenario].reset_index()




# Plot the results
fig, axs = plt.subplots(1, 3, figsize=(16, 4))
axs = axs.ravel()

for i, scenario in enumerate(scenarios):
    # Make a hue for each month but not plotting lines but an area instead
    sns.lineplot(data=df_diurnal[scenario], x='hour', y='Indoor Mean Air Temperature', hue='month', ax=axs[i])
    axs[i].set_title(scenario)
    axs[i].set_ylabel('Monthly Mean Indoor Temperature [°C]')
    axs[i].set_xlabel('Hour')
    axs[i].grid(True)
    axs[i].xaxis.grid(False)
    axs[i].set_ylim([10, 50])
    axs[i].set_xticks(np.arange(0, 24, 6))
    # Change the hue to month names instead of numbers
    axs[i].legend(loc='best')

# Save the figure
plt.savefig('figures/simulations/indoor_mean_air_temperature_diurnal_cycle_3 scenarios.png', dpi=300)
plt.show()


# Using df plot the boxplot for each month and each scenario for Indoor Mean Air Temperature and Indoor Air Relative Humidity using Seaborn

# Plot the results
fig, axs = plt.subplots(1, 3, figsize=(16, 4))
axs = axs.ravel()

for i, scenario in enumerate(scenarios):
    # Replace 0 by RDP house and 1 by Shack house
    df[scenario]['type_house'] = df[scenario]['type_house'].replace(0, 'RDP')
    df[scenario]['type_house'] = df[scenario]['type_house'].replace(1, 'Shack')
    sns.boxplot(data=df[scenario], x='month', y='Indoor Mean Air Temperature', hue='type_house', ax=axs[i])
    sns.swarmplot(data=df[scenario], x='month', y='Indoor Mean Air Temperature', hue='type_house', ax=axs[i], dodge=True, color='black')
    axs[i].set_title(scenario)
    axs[i].set_ylabel('Monthly Mean Indoor Temperature [°C]')
    axs[i].set_xlabel('Month')
    axs[i].grid(True)
    axs[i].xaxis.grid(False)
    axs[i].set_ylim([18, 36])
    axs[i].set_xticks(np.arange(1, 13))
    axs[i].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct','Nov', 'Dec'])
    axs[i].legend(loc='best')


# Import data from machine learning cross validation done with GridSearchCV
df_rf_cv_results = pd.read_csv('results/models/present-day_rf_ml_grid_search_results.csv')
df_bc_cv_results = pd.read_csv('results/models/present-day_bc_ml_grid_search_results.csv')


# Plot params vs mean_test_accuracy for Random Forest (max_depth, min_samples_leaf, min_samples_split, n_estimators)
fig, axs = plt.subplots(2, 2, figsize=(16, 16))
axs = axs.ravel()

for i, param in enumerate(['param_clf__max_depth', 'param_clf__min_samples_leaf', 'param_clf__min_samples_split', 'param_clf__n_estimators']):
    sns.scatterplot(data=df_rf_cv_results, x=param, y='mean_test_accuracy', ax=axs[i])
    param_name = param.split('__')[1]
    axs[i].set_title(param_name)
    axs[i].set_ylabel('Mean Test Accuracy')
    axs[i].set_xlabel(param)
    axs[i].grid(True)
    axs[i].xaxis.grid(False)
    axs[i].set_ylim([0.4, 1.0])
    axs[i].set_xlim([df_rf_cv_results[param].min(), df_rf_cv_results[param].max()])


# Save the figure
plt.savefig('figures/machine_learning/ml_mean_accuracy_params.png', dpi=300)
plt.show()


df_rf_cv_results.info()


df_bc_cv_results.info()


import plotly.express as px
import kaleido as kaleido

# Plot the results for Random Forest

# Create a DataFrame with the results
df_rf_parallel_coord = df_rf_cv_results[['param_clf__max_depth', 'param_clf__min_samples_leaf', 'param_clf__min_samples_split', 'param_clf__n_estimators', 'mean_test_f1_score']]
# Rename the columns
df_rf_parallel_coord.columns = ['Max Depth', 'Min Samples Leaf', 'Min Samples Split', 'N Estimators', 'Mean Test F1 Score']

# Plot the results for having only one line in color for the best result
fig = px.parallel_coordinates(df_rf_parallel_coord, color='Mean Test F1 Score', color_continuous_scale=px.colors.sequential.Reds, range_color=[0.8, 1.0])

# Save the figure

# Show the plot
fig.show()

# Plot the results for Bagger Classifier
# Create a DataFrame with the results
df_bc_parallel_coord = df_bc_cv_results[['param_clf__bootstrap', 'param_clf__bootstrap_features', 'param_clf__max_features', 'param_clf__max_samples', 'param_clf__n_estimators', 'mean_test_f1_score']]

# Rename the columns
df_bc_parallel_coord.columns = ['Bootstrap', 'Bootstrap Features', 'Max Features', 'Max Samples', 'N Estimators', 'Mean Test F1 Score']
# Replace True by 1 and False by 0
df_bc_parallel_coord['Bootstrap'] = df_bc_parallel_coord['Bootstrap'].replace(True, 1)
df_bc_parallel_coord['Bootstrap'] = df_bc_parallel_coord['Bootstrap'].replace(False, 0)
df_bc_parallel_coord['Bootstrap Features'] = df_bc_parallel_coord['Bootstrap Features'].replace(True, 1)
df_bc_parallel_coord['Bootstrap Features'] = df_bc_parallel_coord['Bootstrap Features'].replace(False, 0)
# Plot the results for having only one line in color for the best result
fig = px.parallel_coordinates(df_bc_parallel_coord, color='Mean Test F1 Score', color_continuous_scale=px.colors.sequential.Reds, range_color=[0.8, 1.0])

# Show the plot
# Save the figure

fig.show()



