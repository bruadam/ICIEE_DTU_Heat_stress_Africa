# Author: Bruno Marc J. Adam
# Last Update: 2023-07-04
# Purpose: Script to perform sensitivity analysis on the features used to cluster the data

# University: DTU
# Master Thesis Project: Using AI to predict thermal comfort in buildings in South Africa

import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_selection import mutual_info_classif
from sklearn.model_selection import StratifiedKFold

from toolbox.machine_learning import get_data, get_features_sets
from toolbox.figures import set_dtu_colors, set_matplotlib_style

# Import mutual_info_classif
from sklearn.feature_selection import mutual_info_classif

# Import the necessary modules for plotting
set_matplotlib_style()
colors = set_dtu_colors()


# Import simulation inputs and cluster labels
inputs = pd.read_csv('results/simulations/present-day_inputs.csv', index_col=0)
cluster_labels = pd.read_csv('results/simulations/present-day_cluster_labels.csv', index_col=0)
cluster_labels = cluster_labels.sort_values(by='key').reset_index(drop=True)

# Merge inputs and cluster labels into a single dataframe based on key and index
inputs = inputs.merge(cluster_labels, left_index=True, right_on='key')

# Drop unnecessary columns
inputs.drop(['type_house', 'elec_gas', 'key'], axis=1, inplace=True)


N = [10, 50, 100, 200, 300, len(inputs)]
n_folds = 5  # Number of cross-validation folds

sensitivity_analysis_df = pd.DataFrame()

for n in N:
    mi_scores = []
    skf_outer = StratifiedKFold(n_splits=n_folds, shuffle=True)  # Outer loop for cross-validation
    
    for train_index, test_index in skf_outer.split(inputs.drop('cluster', axis=1), inputs['cluster']):
        sensitivity_df = inputs.copy()
        sensitivity_df = sensitivity_df.sample(n=n)
        X = sensitivity_df.drop('cluster', axis=1)
        y = sensitivity_df['cluster']
        
        skf_inner = StratifiedKFold(n_splits=n_folds, shuffle=True)  # Inner loop for cross-validation
        
        for train_index_inner, test_index_inner in skf_inner.split(X, y):
            X_train, X_test = X.iloc[train_index_inner], X.iloc[test_index_inner]
            y_train, y_test = y.iloc[train_index_inner], y.iloc[test_index_inner]

            mi_scores_fold = mutual_info_classif(X_train, y_train)
            mi_scores.append(mi_scores_fold)
    
    mi_scores = np.array(mi_scores)
    avg_mi_scores = np.mean(mi_scores, axis=0)
    
    sensitivity_analysis = pd.DataFrame({'Features': X.columns, 'Mutual Information': avg_mi_scores})
    sensitivity_analysis.columns = ['Features', n]
    sensitivity_analysis.set_index('Features', inplace=True)

    sensitivity_analysis_df = pd.concat([sensitivity_analysis_df, sensitivity_analysis], axis=1)

    # Print the results
    print("Sensitivity Analysis - Mutual Information Scores for {} samples:\n".format(n))
    print(sensitivity_analysis)
    print("\n")

# Export the results to a CSV file
sensitivity_analysis_df.to_csv('..\\simulations\\sensitivity_analysis.csv', index=False)

sensitivity_analysis_df = sensitivity_analysis_df.sort_values(len(inputs), ascending=False)

# Create the heatmap
sns.heatmap(sensitivity_analysis_df, annot=True, cmap='RdBu_r')

# Name the x axis
plt.xlabel('Number of samples randomly selected within the dataset')

# Save the figure
plt.savefig('figures/sensitivity_analysis/mutual_information.png', dpi=300, bbox_inches='tight')
plt.show()


# Plot line chart with the mutual information scores for each feature
for feature in sensitivity_analysis_df.index:
    plt.plot(N, sensitivity_analysis_df.loc[feature, :])

# Name the x axis
plt.xlabel('Number of samples randomly selected within the dataset')

# Name the y axis
plt.ylabel('Mutual Information Score')
plt.legend(sensitivity_analysis_df.index, loc='center left', bbox_to_anchor=(1, 0.5))
# Save the figure
plt.savefig('figures/sensitivity_analysis/mutual_information_line_chart.png', dpi=300, bbox_inches='tight')
plt.show()


# Calculate the correlation matrix using Pearson's correlation coefficient
correlation_matrix = inputs.corr(method='pearson')

# Plot the correlation matrix as a heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')

# Name the axis
plt.xlabel('Features')
plt.ylabel('Features')
# plt.title("Correlation Matrix - Pearson's Coefficient")

# Save the figure
plt.savefig('figures/sensitivity_analysis/correlation_matrix.png', dpi=300, bbox_inches='tight')
plt.show()


