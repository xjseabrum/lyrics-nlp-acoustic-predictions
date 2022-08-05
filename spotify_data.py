# For this to work on a local machine, 
# be sure to set environment variables in the terminal 
# before opening python:

# Windows:
# $env:SPOTIPY_CLIENT_ID="your_client_id"
# $env:SPOTIPY_CLIENT_SECRET="your_client_secret"

# Mac:
# export SPOTIPY_CLIENT_ID=your_client_id
# export SPOTIPY_CLIENT_SECRET=your_client_secret

# The client and secret id information can be found in your 
# Spotify developer account dashboard application
# https://developer.spotify.com/dashboard/applications

# Spotify API documentation for structuring queries
# https://developer.spotify.com/documentation/web-api/reference/#/operations/search
# However, the example in the official documentation is NOT up to date, instead
# this post on the forums:
# https://community.spotify.com/t5/Spotify-for-Developers/Critical-bug-in-search-API-since-today-or-yesterday/m-p/5203512#M2514
# Shows that the correct joiner is " AND " to combine multiple filters
# in the query.

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

def gather_track_uris(start_year:int, end_year:int, n_tracks:int,
                      genre:str = "r&b", type:str = "album,track") -> list:
    """A function to gather track uris from a given year range, genre, and number of tracks per year.

    Args:
        start_year (int): The start year of the range.
        end_year (int): The end year of the range, inclusive.
        n_tracks (int): The number of tracks to search for per year. Should be less than 300. If not, will set to 300.
        genre (str): The genre to search for.  Defaults to "r&b". Call spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials()).recommendation_genre_seeds() for the full list. 
        type (str): Defaults to "album,track". According to SpotiPy documentation, this is the "types of items to return". The available filters are: "album, artist, track, year, upc, tag:hipster, tag:new, isrc, genre". See the documentation for further details: https://developer.spotify.com/documentation/web-api/reference/#/operations/search

    Returns:
        list: The list of Spotify track uris.
    """               
    track_uris = []
    year_range = [*range(start_year, end_year + 1)]
    YEARS = [str(x) for x in year_range]
    GENRE = genre
    TYPE = type

    # Interestingly, the API doesn't (seem to) allow for more than 300
    # results per query.  Setting the n_track limit to 300.
    if n_tracks > 300:
        print("Setting n_tracks to 300, as the API (seemingly) only allows for 300 results per query.")
        n_tracks = 300

    # This gets the top n_tracks of results for each year
    for year in YEARS:
        print(f"\nProcessing year: {year} for genre: {GENRE}")
        QUERY = f"year:{year} AND genre:{GENRE}"
        
        # The max value accepted by the limit keyword is 50 for spotify's API. 
        # So, we can process in batches of 50 to append to the URI list quicker.
        multiple_of_50 = n_tracks // 50

        # The following is for if we have, ie, 251 tracks, we want to process
        # the next "batch" of 50 tracks.
        if n_tracks % 50 != 0:
            multiple_of_50 += 1

        for offset in range(0, multiple_of_50):
            # For processing less than 50 tracks:
            if n_tracks < 50:
                print(f"Processing tracks {offset*50 + 1}-{n_tracks} of {n_tracks}")
                result = sp.search(QUERY, type = TYPE, limit = n_tracks, 
                                   offset = 0)
                uri_batch = [result['tracks']['items'][x]['uri'].split(":")[2] 
                         for x in range(0, n_tracks)] 
                track_uris += uri_batch
                return track_uris
            
            # If processing the, i.e., 251st track, or some leftover amount that
            # isn't a multiple of 50
            if ((offset + 1)*50) > n_tracks:
                print(f"Processing tracks {offset*50 + 1}-{n_tracks} of {n_tracks}")
                # Offset and limit are adjusted to account for 
                # tracks in a non-full batch of 50.
                result = sp.search(QUERY, type = TYPE, limit = (n_tracks % 50), 
                               offset = (offset*50 - (50 - (n_tracks % 50))))
                uri_batch = [result['tracks']['items'][x]['uri'].split(":")[2] 
                         for x in range(0, (n_tracks % 50))]
                track_uris += uri_batch
                return track_uris                               

            print(f"Processing tracks {offset*50 + 1}-{(offset + 1)*50} of {n_tracks}")
            result = sp.search(QUERY, type = TYPE, limit = 50, 
                                   offset = (offset*50))
            
            # The URI in the JSON file is delimited by colons.
            uri_batch = [result['tracks']['items'][x]['uri'].split(":")[2] 
                         for x in range(0, 50)]                            
            
            # Concatenate the list to have a flat list of URIs.
            track_uris += uri_batch  

    return track_uris

uris = gather_track_uris(start_year = 2013, end_year = 2022, n_tracks = 300)

# pickling the uri list
# import pickle
# with open('uris.pickle', 'wb') as handle:
#     pickle.dump(uris, handle, protocol=pickle.HIGHEST_PROTOCOL)

def get_song_features_from_uri(track_uris:list):
    features_of_interest = {'acousticness', 'danceability', 'energy', 
            'instrumentalness', 'liveness', 'valence', 'speechiness', 'tempo', 
            'duration_ms', 'mode'}
    song_features = []
    uri_idx = 0
    for uri in track_uris:
        print(f"Processing URI #{uri_idx + 1} of {len(track_uris)} URIs")
        audio_features = sp.audio_features(uri)[0]
        result = {key: audio_features[key] for key in features_of_interest}
        song_features.append(result)
        uri_idx += 1
    return song_features

features = get_song_features_from_uri(uris)

# Pickling the features
# with open('features.pickle', 'wb') as handle:
#     pickle.dump(features, handle, protocol=pickle.HIGHEST_PROTOCOL)


# The following function is very slow (~30 min), but it works as intended
# There's very likely a way to do this better.
def get_metadata_info(track_uris:list):
    metadata = []
    uri_idx = 0
    for uri in track_uris:
        print(f"Processing URI #{uri_idx + 1} of {len(track_uris)} URIs")
        track = sp.track(uri)
        track_meta = {}

        track_meta["song_name"] = track["name"]
        track_meta["n_artists"] = len(track["artists"])
        track_meta["main_artist"] = track["artists"][0]["name"]
        track_meta["main_artist_id"] = track["artists"][0]["id"]
        track_meta["main_artist_genres"] = sp.artist(track_meta["main_artist_id"])["genres"]
        track_meta["release_date"] = track["album"]["release_date"]
        track_meta["explicit"] = 1 if track["explicit"] else 0
        metadata.append(track_meta)
        uri_idx += 1
    return metadata

# Pickling the metadata
metadata = get_metadata_info(uris)
with open("metadata.pickle", "wb") as handle:
    pickle.dump(metadata, handle, protocol=pickle.HIGHEST_PROTOCOL)

