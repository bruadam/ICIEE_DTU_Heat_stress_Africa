# Author: Bruno Marc J. Adam
# Last Update: 2023-07-03
# Purpose: Script to perform selection of best machine learning model for the prediction of thermal comfort in buildings in South Africa

# University: DTU
# Master Thesis Project: Using AI to predict thermal comfort in buildings in South Africa

# Selection of a model
from lazypredict.Supervised import LazyClassifier
from joblib import parallel_backend
from sklearn.model_selection import train_test_split
from toolbox.machine_learning import get_data, get_features_sets, balance_data
import warnings
warnings.filterwarnings('ignore')

period = [["2023-01-01 00:00:00" , "2023-01-14 23:00:00"]]
with parallel_backend('threading', n_jobs=4):
    features = {}
    features['simple'] = get_features_sets('simple')
    # Drop light_bulbs
    features['simple'].remove('lighting_bulbs')
    target = 'heat_stress_category'

    X, y = get_data('present-day', features['simple'], target, scaler=True, periods=period)

    # Balance data
    X, y = balance_data(X, y)

    # Print the number of samples for each class
    print('Number of samples for each class:\n {}'.format(y.value_counts()))
    print('Size of the dataset: {}'.format(len(y)))

    # Ask the user if he wants to continue
    input('Press any key to continue...')

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)

    clf = LazyClassifier(verbose=0,ignore_warnings=True, custom_metric=None)
    models, predictions = clf.fit(X_train, X_test, y_train, y_test)
    print(models)

# Save models and predictions
models.to_csv('results/models/ml_comparative_analysis.csv')
predictions.to_csv('results/models/ml_comparative_analysis_predictions.csv')


