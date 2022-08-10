# This is the main entry point for the program.
from setup import *

def main():
    data = create_or_load_data()
    data = add_genius_data(dataset = data)
    data = clean_data(dataset = data)
    data = subset_to_rnb(dataset = data)
    return data

if __name__ == "__main__":
    data = main()

    # For discrete ticks (for the Year variable):
    # https://stackoverflow.com/questions/30112420/histogram-for-discrete-values-with-matplotlib
    # data[["Year", "Month", "Day"]] = data.release_date.str.split("-", expand = True)
    # data["Year"] = data["Year"].astype(int)
    # d = np.diff(np.unique(data.Year)).min()
    # left_of_first_bin = data.Year.min() - float(d)/2
    # right_of_last_bin = data.Year.max() + float(d)/2

    # x = data.Year; plt.hist(x, bins = np.arange(left_of_first_bin, right_of_last_bin + d, d)); plt.title(f"Distribution of `{x.name}`"); plt.xlabel(f"Value, discrete [{np.round(min(x), 1)}, {np.round(max(x), 1)}]    Skew: {np.round(get_skew(x), 3)}, Fisher Kurtosis: {np.round(get_fisher_kurtosis(x), 3)}"); plt.ylabel("Num. occurences"); plt.xticks([2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]); plt.savefig(f"figures_charts/dist_{x.name}.png")