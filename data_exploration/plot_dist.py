import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from utils import fd_bins, get_skew, get_fisher_kurtosis

def get_histogram(dataset, column, 
                  save_plot = True, 
                  folder = "figures_charts/"):
    filename = f"{folder}dist_{column}.png"
    var_of_interest = dataset[column]
    n_bins = fd_bins(var_of_interest)
    plt.hist(var_of_interest, bins = n_bins)
    plt.title(f"Distribution of `{column}`")

    xlabel = f"Value, continuous [{np.round(min(var_of_interest), 1)}, " + \
             f"{np.round(max(var_of_interest), 1)}]    " + \
             f"Skew: {np.round(get_skew(var_of_interest), 3)} " + \
             f"Fisher Kurtosis: {np.round(get_fisher_kurtosis(var_of_interest), 3)}"

    plt.xlabel(xlabel)
    plt.ylabel("Num. occurences")
    if save_plot:
        plt.savefig(filename, bbox_inches = 'tight')
    plt.show()
    plt.close()

def get_corr_heatmap(dataframe, var_type, 
                     folder = "figures_charts/", 
                     save_plot = True):
    name_underscore = var_type.replace(" ", "_")
    filename = f"{folder}corr_{name_underscore}.png"
    var_type_title = var_type.title()
    mask = np.tril(np.ones_like(dataframe.corr()))
    # Fill the diag with 0s to keep the diagonal in the plot.
    np.fill_diagonal(mask, 0)
    plt.figure(figsize = (10, 6))
    heatmap = sns.heatmap(dataframe.corr(),
                          mask = mask,
                          vmin = -1, 
                          vmax = 1, 
                          annot = True, 
                          cmap = 'BrBG')
    heatmap.set_title(f"Correlation Heatmap: {var_type_title}")
    if save_plot:
        plt.savefig(filename, bbox_inches = 'tight')
    plt.show()
    plt.close()
