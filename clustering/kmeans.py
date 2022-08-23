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
from distinctipy import get_colors, get_hex

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

# Optimal number of clusters according to R's NbClust is 3.

# Can use an elbow/knee graph too to determine this. 
inertiae = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=0).fit(x_train_st_emb)
    inertiae.append(kmeans.inertia_)

# Plot
i = np.arange(1, 11)
knee = KneeLocator(i, inertiae, 
                    S = 1, curve = "convex", 
                    direction = "decreasing", 
                    interp_method = "interp1d")
fig2 = plt.figure(figsize=(5, 5))
knee.plot_knee()
plt.xlabel(f"k, knee point is {knee.knee}")
plt.ylabel("inertia")
plt.show()

# Function to use to define the clusters and visualize them
def make_clusters_and_plot(k, data, return_data = False):  
    # Use distinctipy's get_colors and get_hex
    # to get a list of distinct colors automatically
    colors = get_colors(k, pastel_factor = 0.2)
    color_hex = [get_hex(x) for x in colors]
    
    X = data.filter(regex='st_emb_.*')
    kmeans = KMeans(n_clusters = k, random_state = 0).fit(X)
    groupings = kmeans.labels_
    
    
    # TSNE will project the 768-dimensions down to 2 for visualization
    # The projection might look messy as who knows that hyperplanes/spheres are
    # actually separating the clusters.
    tsne = TSNEVisualizer(random_state = 0, colors = color_hex, 
                          alpha = 0.8)
    tsne.fit(X, [f"Cluster: {k}" for k in groupings])
    tsne.show()

    if return_data:
        data["groupings"] = groupings
        return data


# Distinct colors from:
# https://mokole.com/palette.html
# Hex values generated above with [Black OK, 90%] 
# as the luminosity settings with 10000 maximum loops

# Three clusters. Knee and NbClust suggest that so let's use it.
data_3_clusters = make_clusters_and_plot(k = 3, data = x_train,  
                                         return_data = True)
# Five clusters
data_5_clusters = make_clusters_and_plot(k = 5, data = x_train, 
                                         return_data = True)
# Seven Clusters
data_7_clusters = make_clusters_and_plot(k = 7, data = x_train, 
                                         return_data = True)
# Two Clusters
data_2_clusters = make_clusters_and_plot(k = 2, data = x_train, 
                                         return_data = True)