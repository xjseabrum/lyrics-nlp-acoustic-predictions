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

def gather_track_uris(start_year:int = 2018, 
                      end_year:int = 2022, 
                      genre:str = "r&b",
                      type:str = "album,track",
                      n_tracks:int = 200) -> list:
    track_uris = []
    year_range = [*range(start_year, end_year + 1)]
    YEARS = [str(x) for x in year_range]
    GENRE = genre
    TYPE = type
    AND = " AND "

    # We will get the top n_tracks of results for each year
    for year in YEARS:
        print("\n\nProcessing year: " + year + " for genre: " + GENRE)
        QUERY = "year:" + "\"" + year + "\"" + AND + \
                "genre:"+ "\"" + GENRE + "\""

        # Get the top n_tracks of results in the query
        for offset in range(0, n_tracks):
            # Progress meters
            if (offset + 1) % 5 == 0:
                print("Processing track #" + str(offset + 1) + " of " + str(n_tracks))
            elif (offset + 1) % n_tracks == 0:
                print("Processing track #" + str(offset + 1) + " of " + str(n_tracks))
            # There's likely a better way to do this than one by one.
            # Currently, just satisfied that the API calls work as intended.
            result = sp.search(QUERY, type = TYPE, limit = 1, offset = offset)
            # The URI in the JSON file is delimited by colons.
            track_uris.append(result['tracks']['items'][0]['uri'].split(":")[2])   
            
    return track_uris

uris = gather_track_uris()