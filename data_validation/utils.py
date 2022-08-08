import re
import pandas as pd
import matplotlib.pyplot as plt

def stutter_removal(lyrics:str) -> str:
    """
    Remove rhythmic `stutters` from lyrics.
    Ex: "M-M-M-My name is..." -> "My name is..."
    """
    out = re.sub(r"\S?([A-Za-z]\-)+", "", lyrics)
    return out

def remove_genius_embed(lyrics:str) -> str:
    """
    Remove the NUMBERembed that appears at the end of lyrics from Genius.
    Ex: "...yeah176Embed" -> "...yeah"
    """
    out = re.sub(r"([0-9]+)?Embed", "", lyrics)
    return out

def remove_empty_lyrics(dataset:pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows with empty lyrics.
    """
    dataset = dataset[dataset["lyrics"] != ""]
    return dataset

# Function to remove outliers. 
def remove_outliers_using_boxplot(dataset:pd.DataFrame, 
                                 column:str,
                                 first_pass_whisker:float = 1.5,
                                 second_pass_whisker:float = 1.0, 
                                 two_passes = False, 
                                 save_plot = False, 
                                 plot_name = "data") -> pd.DataFrame:
    """
    Remove outliers from a dataset using data from the boxplot.
    """

    # First pass:  filter out outliers that fall outside of 
    # the IQR*first_pass_whisker
    boxplot = plt.boxplot(dataset[column], whis = first_pass_whisker)
    lower_whisker = boxplot["whiskers"][0].get_data()[1][1]
    upper_whisker = boxplot["whiskers"][1].get_data()[1][1]
    outliers = dataset[(dataset[column] < lower_whisker) & 
                       (dataset[column] > upper_whisker)]
    dataset = dataset[~dataset.index.isin(outliers.index)]
    if save_plot:
        # Save the original boxplot
        boxplot.savefig(f"figures_charts/{plot_name}_outlier_pass_00.png")
        # Graph the boxplot again now that the outliers are removed
        boxplot = plt.boxplot(dataset[column], whis = first_pass_whisker)
        boxplot.savefig(f"figures_charts/{plot_name}_outlier_pass_01.png")

    if two_passes:
        # Second pass:  filter out outliers that fall outside of 
        # the IQR*second_pass_whisker
        boxplot = plt.boxplot(dataset[column], whis = second_pass_whisker)
        lower_whisker = boxplot["whiskers"][0].get_data()[1][1]
        upper_whisker = boxplot["whiskers"][1].get_data()[1][1]
        outliers = dataset[(dataset[column] < lower_whisker) & 
                           (dataset[column] > upper_whisker)]
        dataset = dataset[~dataset.index.isin(outliers.index)]
        if save_plot:
            boxplot = plt.boxplot(dataset[column], whis = second_pass_whisker)
            boxplot.savefig(f"figures_charts/{plot_name}_outlier_pass_02.png")
        return dataset
    return dataset

def remove_non_english_lyrics(dataset:pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows with non-English lyrics.
    """
    pass