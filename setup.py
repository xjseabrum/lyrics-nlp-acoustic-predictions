# Setup for running the program in main.

def create_or_load_data():
    from os.path import exists
    import pandas as pd
    from spotify_data import gather_track_uris, get_song_features_from_uri, get_metadata_info, construct_pandas_dataframe
    if not exists("song_data.csv"):
        print("File song_data.csv not found. Creating...")
        uris = gather_track_uris(start_year = 2013, 
                                 end_year = 2022, n_tracks = 300)
        features = get_song_features_from_uri(uris)
        metadata = get_metadata_info(uris)
        data = construct_pandas_dataframe(uris, features, metadata)
        data.to_csv("song_data.csv", index = False)
        print("File song_data.csv has been created.")
    else:
        print("File song_data.csv found. Loading...")
        data = pd.read_csv("song_data.csv")
    return data
    