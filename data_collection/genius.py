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
from data_validation.utils import stutter_removal, remove_genius_embed
genius = Genius(remove_section_headers=True)

def find_lyrics(song_and_artist:list, delimiter = " ::: ") -> str:
    title = song_and_artist.split(delimiter)[0]
    artist = song_and_artist.split(delimiter)[1]
    # Don't need the full info of the song.
    lyrics = genius.search_song(title = title, artist = artist,
                                get_full_info=False)
    # Not all songs have lyrics on genius.
    # If no lyrics, return empty string.
    if lyrics is None:
        return ""
    # Take out the first line break that 
    # contains the song name and artist
    out = lyrics.lyrics.split("\n")[1:]
    # Join the individual string elements back into one string delimited by 
    # \n
    out = "\n".join(out)
    out = stutter_removal(out)
    out = remove_genius_embed(out)
    return out

# The following commented out code is for if the
# internet connection drops randomly.
# This workaround batches the songs in groups of 20.
# However, this requires manual restart as the timeouts can happen at 
# any point.  This temporary solution is not scalable.

# genius_lyrics = []
# batch_size = 20
# n_batches = len(data) // batch_size

# for batch in range(len(genius_lyrics), n_batches):
#     print(f"Processing batch index: {batch} of {n_batches-1}")
#     genius_lyrics.append(
#         np.vectorize(find_lyrics)(
#             data["comb"][(batch*batch_size):((batch+1)*batch_size)]))

# # Flatten the list
# genius_flattened = list(np.concatenate(genius_lyrics).flat)
# data["lyrics"] = genius_flattened
# data["n_words"] = np.vectorize(count_words)(data["lyrics"])
# data.to_csv("data/01_genius_data.csv")





  