import matplotlib.pyplot as plt
import numpy as np
from utils import fd_bins, get_skew, get_fisher_kurtosis

def get_histogram(dataset, column, 
                  save_plot = True, 
                  folder = f"figures_charts/"):
    filename = f"{folder}dist_{column}.png"
    var_of_interest = dataset[column]
    n_bins = min(fd_bins(var_of_interest), 50)
    plt.hist(var_of_interest, bins = n_bins)
    plt.title(f"Distribution of `{column}`")

    xlabel = f"Value, continuous [{np.round(min(var_of_interest), 1)}, " + \
             f"{np.round(max(var_of_interest), 1)}]    " + \
             f"Skew: {np.round(get_skew(var_of_interest), 3)} " + \
             f"Fisher Kurtosis: {np.round(get_fisher_kurtosis(var_of_interest), 3)}"

    plt.xlabel(xlabel)
    plt.ylabel("Num. occurences")
    if save_plot:
        plt.savefig(filename)
    plt.show()
    plt.close()
