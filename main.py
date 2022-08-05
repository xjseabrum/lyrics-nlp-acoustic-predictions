# Ignore this file for now.
# Eventually this will be the main entry point for the program.

from os.path import exists
import pandas as pd
from spotify_data import gather_track_uris, get_song_features_from_uri, get_metadata_info, construct_pandas_dataframe

def main():
    if not exists("song_data.csv"):
        uris = gather_track_uris(start_year = 2013, 
                                 end_year = 2022, n_tracks = 300)
        features = get_song_features_from_uri(uris)
        metadata = get_metadata_info(uris)
        data = construct_pandas_dataframe(uris, features, metadata)
        data.to_csv("song_data.csv", index = False)
    else:
        data = pd.read_csv("song_data.csv")

if __name__ == "__main__":
    main()