import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import fasttext
from utils import count_words
# import spacy
# from spacy.language import Language
# from spacy_langdetect import LanguageDetector

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
    dataset = dataset[dataset[n_words_column] > 0]
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
    return target_language_only