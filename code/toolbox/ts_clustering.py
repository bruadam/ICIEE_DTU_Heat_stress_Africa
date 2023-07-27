import numpy as np
import pandas as pd
import math
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from tslearn.utils import to_time_series_dataset
import matplotlib.pyplot as plt
from toolbox.figures import set_matplotlib_style, set_dtu_colors
from scipy.cluster.hierarchy import inconsistent, maxinconsts
import time
import pickle
colors = set_dtu_colors()
set_matplotlib_style()

def estimation_kmeans_clustering(km, X):
    start = time.time()
    # Fit k-means on 10 first time series
    km.fit(X[:10])
    end = time.time()
    duration = end - start
    estimated_time = duration * len(X) / 10
    print('Estimated time: {} seconds'.format(estimated_time))

# Little handy function to plot series
def plot_som_series_averaged_center(som_x, som_y, win_map):
    import matplotlib.pyplot as plt
    import numpy as np
    fig, axs = plt.subplots(som_x,som_y,figsize=(25,25))
    fig.suptitle('Clusters')
    for x in range(som_x):
        for y in range(som_y):
            cluster = (x,y)
            if cluster in win_map.keys():
                for series in win_map[cluster]:
                    axs[cluster].plot(series,c="gray",alpha=0.5) 
                axs[cluster].plot(np.average(np.vstack(win_map[cluster]),axis=0),c="red")
            cluster_number = x*som_y+y+1
            axs[cluster].set_title(f"Cluster {cluster_number}")

    plt.show()

def plot_som_series_dba_center(som_x, som_y, win_map):
    import matplotlib.pyplot as plt
    from tslearn.barycenters import dtw_barycenter_averaging
    import numpy as np
    fig, axs = plt.subplots(som_x,som_y,figsize=(25,25))
    fig.suptitle('Clusters')
    for x in range(som_x):
        for y in range(som_y):
            cluster = (x,y)
            if cluster in win_map.keys():
                for series in win_map[cluster]:
                    axs[cluster].plot(series,c="gray",alpha=0.5) 
                axs[cluster].plot(dtw_barycenter_averaging(np.vstack(win_map[cluster])),c="red") # I changed this part
            cluster_number = x*som_y+y+1
            axs[cluster].set_title(f"Cluster {cluster_number}")

    plt.show()

def apply_pca_timeseries(df, features, n_components=2, time_series_data=[], pca_data=[]):
    # Apply PCA
    pipeline = Pipeline([
        ('standardize', StandardScaler()),
        ('pca', PCA(n_components=n_components)),
    ])
    transformed_data = pipeline.fit_transform(df[features])
    # Store the 1st principal component in pca_data
    pca_data.append(transformed_data[:, 0])
    time_series_data.append(transformed_data)
    return time_series_data, pca_data

def ts_clustering(df=None, data_path=None, n_clusters=2, plot=False, scenario = 'present-day', method='kmeans'):
    if data_path != None:
        # Read the data
        df = pd.read_csv(data_path)

    if type(df) != dict:  
        df_dict = {}
        for key in df['key'].unique():
            df_dict[key] = df[df['key'] == key]
    else:
        df_dict = df

    time_series_data = []
    pca_data = []
    
    for key in df_dict.keys():
        features = ['Outdoor Dry Bulb Temperature', 'Outdoor Relative Humidity', 'Wind Speed', 'Wind Direction', 'Atmospheric Station Pressure', 'Indoor Mean Air Temperature', 'Indoor Air Relative Humidity', 'Precipitable Water']
        time_series_data, pca_data = apply_pca_timeseries(df=df_dict[key], features=features, n_components=2, time_series_data=time_series_data, pca_data=pca_data)
        

    # Convert the list of time series data into a time series dataset
    X = to_time_series_dataset(time_series_data)
    print(X.shape)

    start = time.time()
    if method == 'kmeans':
        # Compute k-means clustering
        from tslearn.clustering import TimeSeriesKMeans
        km = TimeSeriesKMeans(n_clusters=n_clusters, metric="dtw", max_iter=5, random_state=0)
        estimation_kmeans_clustering(km, X) # Get a estimation of the time it takes to run the algorithm on the full dataset
        km.fit(X)
        # Save the model
        filename = '../results/ts_clustering/'+ scenario + '_kmeans_model.sav'
        pickle.dump(km, open(filename, 'wb'))
        # Get the cluster labels
        cluster_labels = km.labels_
        # Get the cluster centers
        cluster_centers = km.cluster_centers_
        cluster_labels_df = pd.DataFrame({'key': df_dict.keys(), 'cluster': cluster_labels})
        return cluster_labels_df, pca_data, cluster_centers
    if method == 'hierarchical':
        # Compute the linkage matrix
        Z = linkage(X.reshape(X.shape[0], -1), method='ward')
        # Form clusters from the linkage matrix
        cluster_labels = fcluster(Z, t=n_clusters, criterion='maxclust')
        # Save the model
        filename = '../results/ts_clustering/'+ scenario + '_hirarchical_model.sav'
        pickle.dump(Z, open(filename, 'wb'))
        cluster_labels_df = pd.DataFrame({'key': df_dict.keys(), 'cluster': cluster_labels})
        return cluster_labels_df, pca_data
    if method == 'som':
        X_reshaped = X.reshape(X.shape[0], -1)
        from minisom import MiniSom
        som_x = som_y = math.ceil(np.sqrt(n_clusters))
        som = MiniSom(som_x, som_y, X_reshaped.shape[1], sigma=0.3, learning_rate=0.5)
        som.random_weights_init(X_reshaped)
        som.train_batch(X_reshaped, 100)
        # Save the model
        filename = '../results/ts_clustering/'+ scenario + '_som_model.sav'
        pickle.dump(som, open(filename, 'wb'))
        # Get the cluster labels
        cluster_labels = []
        for i in range(len(X)):
            cluster_labels.append(som.winner(X[i])[0]*som_y+som.winner(X[i])[1])
        cluster_labels = np.array(cluster_labels)
        win_map = som.win_map(X)
        plot_som_series_averaged_center(som_x, som_y, win_map)
        cluster_labels_df = pd.DataFrame({'key': df_dict.keys(), 'cluster': cluster_labels})
        return cluster_labels_df, pca_data
    if method == 'som_dba':
        from minisom import MiniSom
        from tslearn.barycenters import dtw_barycenter_averaging
        som_x = som_y = math.ceil(math.sqrt(math.sqrt(len(X))))
        som = MiniSom(som_x, som_y, len(X[0]), sigma=0.3, learning_rate=0.5)
        som.train_batch(X, 100)
        # Save the model
        filename = '../results/ts_clustering/'+ scenario + '_som_dba_model.sav'
        pickle.dump(som, open(filename, 'wb'))
        # Get the cluster labels
        cluster_labels = []
        for i in range(len(X)):
            cluster_labels.append(som.winner(X[i])[0]*som_y+som.winner(X[i])[1])
        cluster_labels = np.array(cluster_labels)
        win_map = som.win_map(X)
        plot_som_series_dba_center(som_x, som_y, win_map)
        cluster_labels_df = pd.DataFrame({'key': df_dict.keys(), 'cluster': cluster_labels})
        return cluster_labels_df, pca_data

    end = time.time()
    print('Time elapsed: {} seconds'.format(end - start))
    

    if plot == True and method == 'hierarchical':
        # Plot the dendrogram
        plt.figure()
        plt.title('[{}] Hierarchical Clustering Dendrogram'.format(scenario))
        dendrogram(Z, leaf_rotation=90., leaf_font_size=4.)
        plt.xlabel('Households time series index')
        plt.ylabel('Distance')
        plt.show()
        
    
    
