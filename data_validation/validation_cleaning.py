# Validating that the lyrics are correct
# and cleaning/finding other sources for instances where they are dubious

import pandas as pd
from data_validation.utils import *

def execute_cleaning(dataset:pd.DataFrame) -> pd.DataFrame:
   # Pipeline for cleaning the data
   dataset = word_count_validation(dataset = dataset)
   dataset = wpm_calculation(dataset = dataset)
   dataset = remove_empty_lyrics(dataset = dataset)
   dataset = remove_outliers_using_boxplot(dataset = dataset, 
                                           two_passes = True, save_plot = True)
   dataset = only_keep_target_language_lyrics(dataset = dataset)
   dataset = remove_duplicate_songs(dataset = dataset)
   dataset = remove_duplicate_songs(dataset = dataset, columns = ["comb"])
   dataset = title_and_artist_in_lyrics(dataset = dataset)
   return dataset
