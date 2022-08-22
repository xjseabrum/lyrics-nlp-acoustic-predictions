# K-Means Clustering
from sklearn.cluster import KMeans

# For bringing in the pickled embeddings from the Google Colab notebook
import pickle
import numpy as np
import pandas as pd

# For visualizing the clusters
import matplotlib.pyplot as plt
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
# or if you already have Python/R interoperability you can use the following:
# optimal_k = R.readRDS('optimal_k.RDS')