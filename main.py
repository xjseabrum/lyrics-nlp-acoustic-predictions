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

    # For discrete ticks (for the Year variable):
    # https://stackoverflow.com/questions/30112420/histogram-for-discrete-values-with-matplotlib
    # data[["Year", "Month", "Day"]] = data.release_date.str.split("-", expand = True)
    # data["Year"] = data["Year"].astype(int)
    # d = np.diff(np.unique(data.Year)).min()
    # left_of_first_bin = data.Year.min() - float(d)/2
    # right_of_last_bin = data.Year.max() + float(d)/2

    # x = data.Year; plt.hist(x, bins = np.arange(left_of_first_bin, right_of_last_bin + d, d)); plt.title(f"Distribution of `{x.name}`"); plt.xlabel(f"Value, discrete [{np.round(min(x), 1)}, {np.round(max(x), 1)}]"); plt.ylabel("Num. occurences"); plt.xticks([2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]); plt.savefig(f"figures_charts/dist_{x.name}.png")