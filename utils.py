# Utility functions for the project

from typing import Iterable, Tuple
import pandas as pd
import re
import math as m
import numpy as np
from os.path import exists
from scipy.stats import skew, kurtosis
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec
from nltk.corpus import stopwords

# If Genius didn't find lyrics/rejected the search, it returns a None type
# Setting the length of those lyrics to be 0. Otherwise, count the number
# of words either delimited by spaces or by new line characters.
def count_words(lyrics:str) -> int:
    if type(lyrics) != str:
        return 0
    if len(lyrics) == 0:
        return 0
    return len(re.split("\n| ", lyrics))

def proportion_unique_words(lyrics:str) -> float:
    # Proportion of unique words in the lyrics
    if type(lyrics) != str:
        return 0
    if len(lyrics) == 0:
        return 0
    return len(set(lyrics.split())) / count_words(lyrics)

def preprocess_text_for_vectorization(lyrics, tokenize = True):
    # Pipeline for preprocessing the text
    # strip punctation, stop word removal, tokenization
    # and vectorization
    if type(lyrics) != list:
        lyrics = list(lyrics)
    lyrics = strip_punctuation(lyrics)
    lyrics = [x.lower() for x in lyrics]
    lyrics = remove_stop_words(lyrics)
    if tokenize:
        lyrics = [x.split() for x in lyrics]
    return lyrics


def remove_stop_words(data_column):
    # Remove stop words from the data_column
    stop_words = set(stopwords.words("english"))
    # Since these are lyrics, it's probably important to keep some 
    # stop words in the lyrics. 
    keep_stops = {"he", "her", "hers", "herself", "his", "i", "me", "my", "myself", "no", "not", "our", "ours", "ourselves", "she", "she's", "them", "they", "we", "you", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"}
    stop_words -= keep_stops
    # Split the lyrics on spaces
    lyrics_removed_stop_words = []
    for lyric in data_column:
        lyric_split = lyric.split()
        lyric_split_no_stop = [x for x in lyric_split if x not in stop_words]
        lyrics_removed_stop_words.append(" ".join(lyric_split_no_stop))
    return lyrics_removed_stop_words

def strip_punctuation(lyrics:list, for_transformers=False):
    # Adjust for non-standard punctuation
    # Left double quote to regular double quote:
    lyrics = [x.replace("&#8220;", "\"") for x in lyrics]
    # lyrics = [x.replace("“", "\"") for x in lyrics]
    # Right double quote to regular double quote:
    lyrics = [x.replace("&#8221;", "\"") for x in lyrics]
    # lyrics = [x.replace("”", "\"") for x in lyrics]
    # Left single quote to regular single quote:
    lyrics = [x.replace("&#8216;", "\'") for x in lyrics]
    # lyrics = [x.replace("‘", "\'") for x in lyrics]
    # Right single quote to regular single quote:
    lyrics = [x.replace("&#8217;", "\'") for x in lyrics]
    # lyrics = [x.replace("â€¦", "\'") for x in lyrics]
    # lyrics = [x.replace("â€™", "\'") for x in lyrics]
    # lyrics = [x.replace("’", "\'") for x in lyrics]
    # Replace other unicode characters with regular space
    lyrics = [x.replace("\u2005", " ") for x in lyrics]
    lyrics = [x.replace("\uffef", " ") for x in lyrics]
    lyrics = [x.replace("\u205f", " ") for x in lyrics]
    lyrics = [x.replace("\n", " ") for x in lyrics]
    if for_transformers:
        punc_strip = "\"#%/:;<=>@[\\]^_`{|}~"
    else:
        punc_strip = "?!\"#%&(),./:;<=>@[\\]^_`{|}~"
    for lyric in range(len(lyrics)):
        specific_lyrics = lyrics[lyric]
        specific_lyrics = specific_lyrics.translate(str.maketrans("", "", punc_strip))
        specific_lyrics = re.sub("  ", " ", specific_lyrics)
        lyrics[lyric] = specific_lyrics
    return lyrics

def fd_bins(data_column):
    # Using the Freedman-Diaconis rule to determine the number of bins
    # https://en.wikipedia.org/wiki/Freedman%E2%80%93Diaconis_rule

    iqr = np.subtract(*np.percentile(data_column, [75, 25]))
    n_obs = len(data_column)
    h = (2 * iqr * (n_obs**(-1/3)))
    max_ = max(data_column)
    min_ = min(data_column)
    # 50 bars is already hard enough to see on a histogram, 
    # so return the minimum between 50 and the number of bins
    return min(50, int(((max_ - min_)/h) // 1))

def get_skew(data_points):
    return skew(data_points, bias = False)

def get_fisher_kurtosis(data_points):
    return kurtosis(data_points, bias = False, fisher = True)

def epsilon_log(column, epsilon = 1e-6):
    # Adds small value epsilon before evaluating the log
    # so as to prevent -Inf in evaluation.  Set value to 
    # 1e-6 or lower.
    value = column + epsilon
    return m.log(value)

def save_split_if_not_exists(data, filepath):
    if not exists(filepath):
        data.to_csv(filepath, index = False)
        print(f"File {filepath} has been created.")
    else:
        print(f"File {filepath} already exists! Delete before trying again.")

def get_mae(y_true, y_pred, average_across_responses = False, precision = 4):
    # Get mae for the 7 response values together
    # Note: sklearn's mae returns a warning to screen 
    # due to a deprication issue on their end.  
    # However, the results calculations below match sklearn's 
    # all without producing the warning.
    if average_across_responses:
        # Take the flat average of the mae across the 7 response values
        out = np.mean(np.abs(y_true - y_pred), axis = 1).mean()
        return np.round(out, precision)
    out = np.array(np.mean(np.abs(y_true - y_pred), axis = 0)).reshape(1, -1)
    return np.round(out, precision)

def get_mse(y_true, y_pred, average_across_responses = False):
    # Get mae for the 7 response values together
    # Note: sklearn's mae returns a warning to screen 
    # due to a deprication issue on their end.  
    # However, the results calculations below match sklearn's 
    # all without producing the warning.
    if average_across_responses:
        # Take the flat average of the mae across the 7 response values
        return np.mean(np.square(y_true - y_pred), axis = 1).mean()
    return np.array(np.mean(np.square(y_true - y_pred), axis = 0)).reshape(1, -1)

def get_rmse(y_true, y_pred, average_across_responses = False, precision = 4):
    if average_across_responses:
        out = np.sqrt(get_mse(y_true, y_pred, average_across_responses))
        return np.round(out, precision)
    out = np.sqrt(get_mse(y_true, y_pred, average_across_responses))
    return np.round(out, precision)

def calculate_tfidf(lyrics:list) -> Tuple[pd.DataFrame, list, pd.DataFrame]:
    # sklearn's vectorizer removes stopwords based on frequency of word occurence
    # across all documents if a stop word list is not specified.
    # It also will automatically lowercase all words.

    # First, strip the lyrics of punctuation and newlines. Strip punctuation
    # function is user defined above.
    lyrics = strip_punctuation(lyrics)

    vectorizer = TfidfVectorizer()

    # Initialize and fit->transform the lyrics
    tfidf = vectorizer.fit_transform(lyrics)

    # The following is the idf calculation for all non-stop terms in the corpus
    idf = pd.DataFrame(vectorizer.idf_, index = vectorizer.get_feature_names_out(), columns = ["idf_value"])

    # Get the sparse ``Tf-idf-weighted document-term matrix.``
    sparse_matrix = pd.DataFrame(tfidf[0:(tfidf.shape[0])].toarray(), 
                                 columns = vectorizer.get_feature_names_out())

    # Also get the dense CSR representation for the documents
    csr_format_representation = []
    for lyric in range(len(lyrics)):
        csr_format_representation.append(tfidf[lyric].data)

    return sparse_matrix, csr_format_representation, idf

def create_w2v(lyrics:Iterable, vector_size = 200, min_count = 5) -> Word2Vec:
    # Create the word2vec model
    # the gensim library will take care of the heavy lifting
    # and return a model object.

    # Using a custom defined preprocess_text_for_vectorization function
    lyrics = preprocess_text_for_vectorization(lyrics, tokenize = True)
    w2v_model = Word2Vec(lyrics, min_count = min_count, 
                         vector_size = vector_size)
    print(f"W2V created {vector_size}-dimensional vectors " 
          f"with {len(w2v_model.wv)} word(s) in the vocab.")
    return w2v_model

# def lyric_vectorizer():
#     vectorizer = TextVectorization(max_tokens = 4096,
#                                    output_sequence_length = 256)
#     pass
