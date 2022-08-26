# EM Algorithm with sklearns GaussianMixture
from sklearn.mixture import GaussianMixture

# For bringing in the pickled embeddings from the Google Colab notebook
import pickle
from utils import setup_legible_numbers
from clustering.utils import plot_clusters
import pandas as pd

# Bring in the data that were saved when testing out k-means.
setup_legible_numbers()
x_train_st_emb = pd.read_csv('data/05_x_train_st_emb.csv')

# Select just the columns that are floats
embeddings = x_train_st_emb.filter(regex='st_emb_.*')

# Some cluster numbers to try
# 3, 7, and at most n_obs // 30 
# (as I would like to try have at least 30 obs per cluster)
max_clusters = len(embeddings) // 30

# Run the GMMs and see that they converged.
gmm_3 = GaussianMixture(n_components = 3, random_state = 0).fit(embeddings)
gmm_7 = GaussianMixture(n_components = 7, random_state = 0).fit(embeddings)
gmm_max = GaussianMixture(n_components = max_clusters, 
                          random_state = 0).fit(embeddings)

print(f"Converged?:\n" + 
      f"3: {gmm_3.converged_};\n" + 
      f"7: {gmm_7.converged_};\n" + 
      f"max: {gmm_max.converged_}")

# Capture the top 2 most likely clusters for each row
# and the probability of each cluster
# Post Note:  For these data, EM seems to be very confident in its clusters, 
# and returns probabilities that are exactly 1.0 or 0.0.
# This is most likely due to the high dimensonality of these data. 
cluster_probs_3 = gmm_3.predict_proba(embeddings)
cluster_probs_7 = gmm_7.predict_proba(embeddings)
cluster_probs_max = gmm_max.predict_proba(embeddings)

cluster_probs_3 = pd.DataFrame(cluster_probs_3)
cluster_probs_3.columns = [f'3emclusterprob_{i}' for i in range(3)]
cluster_probs_3["top_cluster"] = cluster_probs_3.idxmax(axis = 1)
cluster_probs_3["top_cluster_prob"] = cluster_probs_3.max(axis = 1, 
                                                          numeric_only = True)

cluster_probs_7 = pd.DataFrame(cluster_probs_7)
cluster_probs_7.columns = [f'7emclusterprob_{i}' for i in range(7)]
cluster_probs_7["top_cluster"] = cluster_probs_7.idxmax(axis = 1)
cluster_probs_7["top_cluster_prob"] = cluster_probs_7.max(axis = 1,
                                                            numeric_only = True)

cluster_probs_max = pd.DataFrame(cluster_probs_max)
cluster_probs_max.columns = [f'{max_clusters}emclusterprob_{i}' 
                               for i in range(max_clusters)]
cluster_probs_max["top_cluster"] = cluster_probs_max.idxmax(axis = 1)
cluster_probs_max["top_cluster_prob"] = cluster_probs_max.max(axis = 1,
                                                            numeric_only = True)

# Renaming the object to be more consistent with its usage.
x_train_clusters = x_train_st_emb.copy(deep = True)

# The following is to just get the number from the string in each
# of the column names
def split_return_number(string_):
    return int(string_.split('_')[1])

x_train_clusters["em3"] = cluster_probs_3["top_cluster"].apply(split_return_number)
x_train_clusters["em7"] = cluster_probs_7["top_cluster"].apply(split_return_number)
x_train_clusters[f"em{max_clusters}"] = cluster_probs_max["top_cluster"].apply(split_return_number)

# Using an altered version of the make_clusters_and_plot function
# from clustering\utils.py
# Function takes in a dataframe, expects a single column name (str)
# and will make the plot.  Necessitates that the clustering has already been
# done and the column name is in the dataframe.
plot_clusters(x_train_clusters, "em3")
plot_clusters(x_train_clusters, "em7")
plot_clusters(x_train_clusters, f"em{max_clusters}")
plot_clusters(x_train_clusters, "3kmeans")
plot_clusters(x_train_clusters, "7kmeans")

# Save these models so that they can be used to classify
# on unseen data:
with open('models/gmm_3.pkl', 'wb') as f:
    pickle.dump(gmm_3, f, pickle.HIGHEST_PROTOCOL)
with open('models/gmm_7.pkl', 'wb') as f:
    pickle.dump(gmm_7, f, pickle.HIGHEST_PROTOCOL)
with open('models/gmm_20.pkl', 'wb') as f:
    pickle.dump(gmm_max, f, pickle.HIGHEST_PROTOCOL)

# Save the newly added clusters to a csv
x_train_clusters.to_csv('data/06_x_train_clusters.csv', index = False)

# Pivot tables.
x_train_clusters["count"] = 1
pd.pivot_table(data = x_train_clusters[["em3", "3kmeans", "count"]], 
               columns = "em3", index = "3kmeans", values = "count", 
               aggfunc = "count", fill_value = 0)
        
#          em3 
#            0    1    2
# 3kmeans
# 0         38  226    1
# 1        126    5   12
# 2          0   22  180

pd.pivot_table(data = x_train_clusters[["em7", "7kmeans", "count"]], 
               columns = "em7", index = "7kmeans", values = "count", 
               aggfunc = "count", fill_value = 0)

#         em7
#           0   1   2   3   4   5   6
# 7kmeans
# 0        12  17   0   0   9   6   1
# 1         2  29   2   7  63   0   0
# 2         0   0  69  11  10   0  12
# 3        41   3   0  21   6   9   0
# 4         3   0   0   0   4  59  12
# 5         0   3   5   0  13   0  68
# 6         0   3   0  89  19   2   0


# # Read in the other pickled data from the Google Colab notebook
# with open('Google_Colab_Notebooks/x_valid_st_emb.pkl', 'rb') as f:
#     x_valid_st_emb = pickle.load(f)
#     x_valid_st_emb = pd.DataFrame(x_valid_st_emb)
#     x_valid_st_emb.columns = [f'st_emb_{i}' for i in range(len(x_valid_st_emb.columns))]


