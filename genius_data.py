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

import numpy as np
from lyricsgenius import Genius
from utils import stutter_removal, remove_genius_embed
genius = Genius(remove_section_headers=True)

def find_lyrics(song_and_artist:list, delimiter = " ::: ") -> str:
    # Then get the song with the most similar track title name
    title = song_and_artist.split(delimiter)[0]
    artist = song_and_artist.split(delimiter)[1]
    # Don't need the full info of the song.
    lyrics = genius.search_song(title = title, artist = artist,
                                get_full_info=False)
    # Take out the first line break that 
    # contains the song name and artist
    out = lyrics.lyrics.split("\n")[1:]
    # Join the individual string elements back into one string delimited by 
    # \n
    out = "\n".join(out)
    out = stutter_removal(out)
    out = remove_genius_embed(out)
    return out

# np.vectorize(find_lyrics)(data["comb"])    
  