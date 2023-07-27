# Author: Bruno Marc J. Adam
# Last Update: 2023-07-03
# Purpose: Script to perform machine learning on the data of the present-day scenario using the best performing models (RandomForestClassifier, BaggingClassifier) and save the results (best model, grid search results, best parameters) in csv files

# University: DTU
# Master Thesis Project: Using AI to predict thermal comfort in buildings in South Africa

# Import libraries
import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings('ignore')

from toolbox.machine_learning import get_features_sets, get_data, balance_data


# Get features
features = get_features_sets('Aggregated')

# Get data
scenario = 'present-day'
target = 'heat_stress_category'

X, y = get_data(scenario, features, target, scaler=True, periods=[['2023-01-01 00:00:00', '2023-01-07 23:00:00']])

# Balance data
X, y = balance_data(X, y)

# Save data
pd.concat([X, y], axis=1).to_csv('results/models/' + scenario + '_ml_data.csv', index=False)


import pickle
# Refine best performing models on X, y using a pipeline
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

# Import 2 models (RandomForestClassifier, BaggingClassifier)
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier

# Define metrics
from sklearn.metrics import make_scorer, f1_score, accuracy_score, precision_score, recall_score

# Define scoring
scoring = {'accuracy': make_scorer(accuracy_score),
              'precision': make_scorer(precision_score, average='weighted', zero_division=1),
                'recall': make_scorer(recall_score, average='weighted'),
                    'f1_score': make_scorer(f1_score, average='weighted')}

# Define a pipeline
pipeline = Pipeline([
    ('clf', RandomForestClassifier())
])

# Define hyperparameters
hyperparameters = {
    'clf__n_estimators': [100, 200, 300],
    'clf__max_depth': [None, 5, 10, 20],
    'clf__min_samples_split': [2, 4, 6],
    'clf__min_samples_leaf': [1, 2, 4]
}

# Define grid search
clf = GridSearchCV(pipeline, hyperparameters, scoring=scoring, refit='f1_score', cv=5, verbose=0, n_jobs=-1)

# Fit and tune model
clf.fit(X, y)

# Save the best model
best_model = clf.best_estimator_
pickle.dump(best_model, open('results/models/' + scenario + '_rf_ml_best_model.sav', 'wb'))

# Save the results of the grid search
pd.DataFrame(clf.cv_results_).to_csv('results/models/' + scenario + '_rf_ml_grid_search_results.csv', index=False)

# Save the best parameters
pd.DataFrame(clf.best_params_, index=[0]).to_csv('results/models/' + scenario + '_rf_ml_best_params.csv', index=False)


# Define a pipeline
pipeline = Pipeline([
    ('clf', BaggingClassifier())
])

# Define scoring
scoring = {'accuracy': make_scorer(accuracy_score),
              'precision': make_scorer(precision_score, average='weighted', zero_division=1),
                'recall': make_scorer(recall_score, average='weighted'),
                    'f1_score': make_scorer(f1_score, average='weighted')}

# Define hyperparameters
hyperparameters = {
    'clf__n_estimators': [100, 200, 300],
    'clf__max_samples': [0.5, 0.75, 1.0],
    'clf__max_features': [0.5, 0.75, 1.0],
    'clf__bootstrap': [True, False],
    'clf__bootstrap_features': [True, False]
}

# Define grid search
clf = GridSearchCV(pipeline, hyperparameters, scoring=scoring, refit='f1_score', cv=5, verbose=0, n_jobs=-1)

# Fit and tune model
clf.fit(X, y)

# Save the best model
best_model = clf.best_estimator_
pickle.dump(best_model, open('results/models/' + scenario + '_bc_ml_best_model.sav', 'wb'))

# Save the results of the grid search
pd.DataFrame(clf.cv_results_).to_csv('results/models/' + scenario + '_bc_ml_grid_search_results.csv', index=False)

# Save the best parameters
pd.DataFrame(clf.best_params_, index=[0]).to_csv('results/models/' + scenario + '_bc_ml_best_params.csv', index=False)


