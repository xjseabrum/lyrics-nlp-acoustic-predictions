import ast
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import fasttext
from utils import count_words

def stutter_removal(lyrics:str) -> str:
    """
    Remove rhythmic `stutters` from lyrics.
    Ex: "M-M-M-My name is..." -> "My name is..."
    """
    out = re.sub(r"\S?([A-Za-z]\-)+", "", lyrics)
    return out

def title_and_artist_in_lyrics(dataset:pd.DataFrame, 
                               title_artist:str = "comb", 
                               lyrics:str = "lyrics") -> pd.DataFrame:
    
    """
    Check if the title and artist are in the lyrics. If they are, 
    very likely that the ``lyrics`` are some type of list of artists and songs.
    """
    dataset.reset_index(drop = True, inplace = True)
    title_artist_list = [re.sub(" ::: ", " - ", x) for x in dataset[title_artist]]
    drop_observation = []
    for item in range(len(title_artist_list)):
        if (title_artist_list[item]) in dataset[lyrics].get(item):
            drop_observation.append(1)
        elif "feat." in dataset[lyrics].get(item):
            drop_observation.append(1)
        else:
            drop_observation.append(0)
    dataset["drop"] = drop_observation
    dataset = dataset[dataset["drop"] == 0]
    dataset = dataset.drop(columns = ["drop"])
    return dataset

def remove_genius_embed(lyrics:str) -> str:
    """
    Remove the NUMBERembed that appears at the end of lyrics from Genius.
    Ex: "...yeah176Embed" -> "...yeah"
    """
    out = re.sub(r"([0-9]+(.|,)?([0-9]+)?(K|M|B)?)?Embed", "", lyrics)
    return out

def word_count_validation(dataset:pd.DataFrame, column = "lyrics"):
    """Counts the number of words in each song's lyrics

    Args:
        dataset (pd.DataFrame): _description_
        column (str, optional): _description_. Defaults to "lyrics".

    Returns:
        _type_: _description_
    """
    n_words = []
    for item in dataset[column]:
        n_words.append(count_words(item))
    dataset["n_words"] = n_words
    return dataset

def wpm_calculation(dataset:pd.DataFrame, 
                    duration_column = "duration_ms", 
                    n_words_column = "n_words"):
    """
    Calculate the words per minute (wpm) for each song. Assumes that the
    duration of each song is in milliseconds and calculates `duration_min`.
    """
    dataset["duration_min"] = dataset[duration_column] / 60000
    dataset["wpm"] = dataset[n_words_column] / dataset["duration_min"]
    return dataset
    

def remove_empty_lyrics(dataset:pd.DataFrame, 
                        n_words_column = "n_words") -> pd.DataFrame:
    """
    Remove rows with empty lyrics.
    """
    dataset = dataset[(dataset[n_words_column] > 0) & 
                      (dataset[n_words_column] != np.nan)]
    return dataset

def remove_duplicate_songs(dataset:pd.DataFrame, 
                           columns:list = ["track_id"]) -> pd.DataFrame:
    dataset = dataset.drop_duplicates(subset = columns)
    return dataset

# Function to remove outliers. 
def remove_outliers_using_boxplot(dataset:pd.DataFrame, 
                                 data_column:str = "wpm",
                                 first_pass_whisker:float = 1.5,
                                 second_pass_whisker:float = 1.0, 
                                 two_passes = True, 
                                 save_plot = False, 
                                 plot_name = "data") -> pd.DataFrame:
    """
    Remove outliers from a dataset using data from the boxplot.
    """

    # First pass:  filter out outliers that fall outside of 
    # the IQR*first_pass_whisker
    if save_plot:
        plt.boxplot(dataset[data_column], whis = first_pass_whisker)
        plt.savefig(f"figures_charts/{plot_name}_outlier_pass_00.png")
        plt.close()

    boxplot = plt.boxplot(dataset[data_column], whis = first_pass_whisker)
    lower_whisker = boxplot["whiskers"][0].get_data()[1][1]
    upper_whisker = boxplot["whiskers"][1].get_data()[1][1]
    dataset = dataset[(dataset[data_column] >= lower_whisker) & 
                       (dataset[data_column] <= upper_whisker)]
    plt.close()

    if save_plot:
        # Graph the boxplot again now that the outliers are removed
        plt.boxplot(dataset[data_column], whis = first_pass_whisker)
        plt.savefig(f"figures_charts/{plot_name}_outlier_pass_01.png")
        plt.close()

    if two_passes:
        # Second pass:  filter out outliers that fall outside of 
        # the IQR*second_pass_whisker.  The first pass got rid of high outliers,
        # this pass will get rid of low outliers.
        boxplot = plt.boxplot(dataset[data_column], whis = second_pass_whisker)
        lower_whisker = boxplot["whiskers"][0].get_data()[1][1]
        dataset = dataset[(dataset[data_column] >= lower_whisker)]
        plt.close()
        boxplot = plt.boxplot(dataset[data_column], whis = first_pass_whisker)
        upper_whisker = boxplot["whiskers"][1].get_data()[1][1]
        dataset = dataset[(dataset[data_column] <= upper_whisker)]
        plt.close()

        if save_plot:
            plt.boxplot(dataset[data_column], whis = second_pass_whisker)
            plt.savefig(f"figures_charts/{plot_name}_outlier_pass_02.png")
            plt.close()
        return dataset
    return dataset

def only_keep_target_language_lyrics(dataset:pd.DataFrame, 
                                     column="lyrics", 
                                     target_language:list=["en"]) -> pd.DataFrame:
    """
    Only keep rows that are in the target language(s).
    """
    # This line is to prevent the fasttext warning from printing to screen:
    # Warning : `load_model` does not return WordVectorModel or SupervisedModel any more, but a `FastText` object which is very similar.
    fasttext.FastText.eprint = lambda x: None

    # Create the model and use it for predictions
    fasttext_model = fasttext.load_model("data_validation/lid.176.ftz")
    lang_predictions = []
    for text in dataset[column]:
        # Remove the newline character from the text so the model can predict
        text = text.replace("\n", "")
        # The last 2 characters are the language code.
        lang_predictions.append(fasttext_model.predict(text)[0][0][-2:])
    dataset["lyrics_lang"] = lang_predictions
    target_language_only = dataset[dataset["lyrics_lang"].isin(target_language)]
    target = target_language_only.drop(columns = ["lyrics_lang"])
    return target

# Filter the dataset to artists whose genres are at least comprised 
# of half rnb or its variants.
def half_rnb(s):
    # If half of the artist's genres are R&B, return true
    s_list = ast.literal_eval(s)
    n_genre = len(s_list)
    n_rnb = 0
    for item in s_list:
        if "r&b" in item.lower():
            n_rnb += 1
    return n_rnb >= 0.5*n_genre