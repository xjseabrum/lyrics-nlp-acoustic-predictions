# DBSCAN
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from sqlalchemy import desc
from utils import setup_legible_numbers
from clustering.utils import plot_clusters
from collections import Counter

# Load the embeddings from the Google Colab notebook
# Bring in the data that were saved when testing out k-means.
setup_legible_numbers()
x_train = pd.read_csv('data/06_x_train_clusters.csv')

# Select the embedding columns
embeddings = x_train.filter(regex='st_emb_.*')

# Determine the optimal distance threshold for the DBSCAN
# see how far away nearest neighbors are in the embedding space
neighbors = NearestNeighbors(n_neighbors = len(embeddings)).fit(embeddings)
dist, idx = neighbors.kneighbors(embeddings)
max_dist = dist[:, -1]

# Sorting in reverse order on a numpy array
# Iterate starting from the back of the array and sort from there.
# This operation happens in place  
max_dist[::-1].sort()

# Use the knee locator to determine the optimal eps value
from kneed import KneeLocator
i = range(0, len(max_dist))
knee = KneeLocator(i, max_dist, 
                    S = 1, curve = "convex", 
                    direction = "decreasing", 
                    interp_method = "interp1d")
knee.plot_knee()
plt.xlabel(f"k, knee point is {knee.knee}\n" +  
           f"distance={max_dist[knee.knee]:.3f} at index: {knee.knee}")
plt.ylabel("distance")
plt.show()
# The value of knee.knee is the index of the optimal eps value
optimal_eps = max_dist[knee.knee]

# Run the DBSCAN
# Default values are: eps = 0.5, min_samples = 5.  Try to keep min samples > 2.
# A cluster value of -1 indicates an outlier.
dbscan = DBSCAN(eps = optimal_eps, min_samples = 5, metric = "euclidean")
model = dbscan.fit(embeddings)
print(set(model.labels_))


# The knee locator isn't good for this data. 
# Let's try a different way. Let's use the min distance.
min_dist = max_dist.min()
alt_min = min_dist / 2 + 0.3
dbscan = DBSCAN(eps = alt_min, min_samples = 5, metric = "euclidean")
model = dbscan.fit(embeddings)
print(set(model.labels_))
counter = Counter(model.labels_)
print(counter)

# With alt_min = min_dist / 2 + 0.08
# Alt_min = 0.67867...
# >>> Counter({-1: 567, 0: 24, 1: 19})
# Anything above +0.09 results in groupings of 0 and -1.
# Add to dataframe and plot.
x_train['dbscan_0.08'] = model.labels_

# With +0.18, this is a rough break even point:
# Alt_min = 0.76867...
# >>> Counter({0: 376, -1: 234})
# Add to dataframe and plot.
x_train['dbscan_0.18'] = model.labels_

# At values above 0.3, few identified outliers.
# Alt_min = 0.89878...
# >>> Counter({0: 589, -1: 21})
# Add to dataframe and plot.
x_train['dbscan_0.3'] = model.labels_

plot_clusters(x_train, "dbscan_0.08")
plot_clusters(x_train, "dbscan_0.18")
plot_clusters(x_train, "dbscan_0.3")