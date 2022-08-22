# K-Means Clustering
from sklearn.cluster import KMeans

# For bringing in the pickled embeddings from the Google Colab notebook
import pickle
import numpy as np
import pandas as pd

# For visualizing the clusters
import matplotlib.pyplot as plt
from kneed import KneeLocator
from yellowbrick.text import TSNEVisualizer

# Load the embeddings from the Google Colab notebook
with open('Google_Colab_Notebooks/x_train_st_emb.pkl', 'rb') as f:
    x_train_st_emb = pickle.load(f)

x_train = pd.read_csv('data/05_x_train.csv')

# Add the embeddings to the dataframe
x_train_st_emb = pd.DataFrame(x_train_st_emb)
x_train_st_emb.columns = ['st_emb_' + str(i) for i in range(x_train_st_emb.shape[1])]
x_train = x_train.merge(x_train_st_emb, left_index=True, right_index=True)

# Save this as a csv for use in R in a bit.
x_train.to_csv('data/05_x_train_st_emb.csv')

# Determine the best number of clusters with R's NbClust
# switch over to the optimal_k.R file for this
# or if you already have the ``reticulate`` package in R 
# or the ``rpy2`` library in Python, you can more easily 
# interoperate between Python and R.

# Optimal number of clusters according to NbClust is 3.
# Can use an elbow/knee graph too. 

inertias = []
for k in range(2, 10):
    kmeans = KMeans(n_clusters=k, random_state=0).fit(x_train_st_emb)
    print(k, kmeans.inertia_)
    inertias.append(kmeans.inertia_)

# Plot
i = np.arange(len(inertias))
for idx in range(i):
    knee = KneeLocator(i, self.distortions, 
                        S = 1, curve='convex', 
                        direction='decreasing', 
                        interp_method='interp1d')
    fig2 = plt.figure(figsize=(5, 5))
    self.knee.plot_knee()
    plt.xlabel("k")
    plt.ylabel("Distortion")


kmeans = KMeans(n_clusters=3, random_state=0).fit(x_train_st_emb)
groupings = kmeans.labels_