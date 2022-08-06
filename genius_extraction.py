# Get lyrics using Genius API

# Genius also requires access tokens to use their API.
# Instructions here: https://lyricsgenius.readthedocs.io/en/master/setup.html#setup

# Similar to setting up with Spotify's API, 
# set up the access token in terminal
# before opening python:

# Windows:
# $env:GENIUS_ACCESS_TOKEN="your_access_token"

# Mac:
# export GENIUS_ACCESS_TOKEN=your_access_token

# These can be found in your api client in Genius:
# https://genius.com/api-clients

from lyricsgenius import Genius
genius = Genius()

def find_lyrics():
    
    pass
