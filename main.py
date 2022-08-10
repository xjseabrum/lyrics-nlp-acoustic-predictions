# This is the main entry point for the program.
from setup import *

def main():
    data = create_or_load_data()
    data = add_genius_data(dataset = data)
    data = clean_data(dataset = data)
    data = assert_rnb(dataset = data)
    return data

if __name__ == "__main__":
    data = main()

    # The following is to generate the histograms
    # fd_bins reports over 6k bins for instrumentalness, so that was manually
    # set to 40. Otherwise fd_bins worked fine.
    # x = data.acousticness; plt.hist(x, bins = fd_bins(x)); plt.title(f"Distribution of `{x.name}`"); plt.xlabel(f"Value, continuous [{np.round(min(x), 1)}, {np.round(max(x), 1)}]"); plt.ylabel("Num. occurences"); plt.savefig(f"figures_charts/dist_{x.name}.png")