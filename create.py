# Setup file for running the program in main.
from os.path import exists
import pandas as pd
import numpy as np
from data_collection.spotify import *
from data_collection.genius import find_lyrics
from data_validation.utils import half_rnb
from data_validation.validation_cleaning import execute_cleaning

def create_or_load_data(filepath = "data/00_song_data.csv") -> pd.DataFrame:
    if not exists(filepath):
        print(f"File {filepath} not found. Creating...")
        uris = gather_track_uris(start_year = 2013, 
                                 end_year = 2022, n_tracks = 300)
        features = get_song_features_from_uri(uris)
        metadata = get_metadata_info(uris)
        data = construct_pandas_dataframe(uris, features, metadata)
        data.to_csv(f"{filepath}", index = False)
        print(f"File {filepath} has been created.")
    else:
        print(f"File {filepath} found. Loading...")
        data = pd.read_csv(f"{filepath}")
    return data

def add_genius_data(dataset:pd.DataFrame, 
                    genius_filepath = "data/01_genius_data.csv") -> pd.DataFrame:
    data = dataset
    if not exists(genius_filepath):
        print(f"File {genius_filepath} not found. Creating...")
        data["lyrics"] = np.vectorize(find_lyrics)(data["comb"])
        data.to_csv("data/01_genius_data.csv", index = False)
        print(f"File {genius_filepath} has been created.")
    else:
        print(f"File {genius_filepath} found. Loading...")
        data = pd.read_csv(f"{genius_filepath}")
    return data

def clean_data(dataset:pd.DataFrame, 
               clean_filepath = "data/02_data_clean.csv") -> pd.DataFrame:
    data = dataset
    if not exists(clean_filepath):
        print(f"File {clean_filepath} not found. Creating...")
        data = execute_cleaning(dataset = data)
        data.to_csv(f"{clean_filepath}", index = False)
        print(f"File {clean_filepath} has been created.")
    else:
        print(f"File {clean_filepath} found. Loading...")
        data = pd.read_csv(f"{clean_filepath}")
    data = data.reset_index(drop = True)
    return data
    
def subset_to_rnb(dataset:pd.DataFrame, 
               clean_filepath = "data/03_rnb_songs.csv") -> pd.DataFrame:
    data = dataset
    if not exists(clean_filepath):
        print(f"File {clean_filepath} not found. Creating...")
        data["rnb"] = data["main_artist_genres"].apply(half_rnb)
        rnb = data[data["rnb"]]
        rnb = rnb.drop(columns = ["rnb"])
        rnb.to_csv(f"{clean_filepath}", index = False)
        print(f"File {clean_filepath} has been created.")
    else:
        print(f"File {clean_filepath} found. Loading...")
        rnb = pd.read_csv(f"{clean_filepath}")
    rnb = rnb.reset_index(drop = True)
    return rnb