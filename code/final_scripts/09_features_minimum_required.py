# Author: Bruno Marc J. Adam
# Last Update: 2023-07-03
# Purpose: Script to perform a feature selection and cross-validation on the simulation data to evaluate the minimum number of features needed to predict thermal comfort with good accuracy

# University: DTU
# Master Thesis Project: Using AI to predict thermal comfort in buildings in South Africa

# Perform feature selection and cross-validation
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import cross_val_score
from toolbox.machine_learning import balance_data
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from toolbox.machine_learning import get_features_sets, get_data
from toolbox.figures import figure_params
import pandas as pd

# Define target
target = 'heat_stress_category'

# Define period
period = [["2023-01-01 00:00:00" , "2023-01-31 23:00:00"]] # January 2023

# Get features sets
features = get_features_sets('Aggregated')

# Get data
X, y = get_data('present-day', features, target, scaler=True, periods=period)

# Balance data
X, y = balance_data(X, y)

columns = X.columns

# Train a RandomForestClassifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X, y)

# Get feature importances
importances = clf.feature_importances_

# Perform feature selection
selector = SelectFromModel(clf, threshold=0.05, )
X_transformed = selector.transform(X)

# Get selected features
selected_features = columns[selector.get_support()]
print('Selected features: ', selected_features)

# Perform cross-validation on the selected features
X_train, X_test, y_train, y_test = train_test_split(X_transformed, y, test_size=0.2, random_state=42)

scores = cross_val_score(clf, X_train, y_train, cv=5)

print("Cross-validation scores: ", scores)
print("Average cross-validation score: ", scores.mean())

# Save feature importances
df = pd.DataFrame(importances, index=columns, columns=['importance'])
df.to_csv('results/features/feature_importances.csv')

# Save selected features
df = pd.DataFrame(selected_features, columns=['selected_features'])
df.to_csv('results/features/selected_features.csv')

# Save cross-validation scores
df = pd.DataFrame(scores, columns=['cross_validation_scores'])
df.to_csv('results/features/cross_validation_scores.csv')


