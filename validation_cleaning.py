# Validating that the lyrics are correct
# and cleaning/finding other sources for instances where they are dubious

import numpy as np
import re
import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv("data_genius_data.csv")

# If Genius didn't find lyrics/rejected the search, it returns a None type
# Setting the length of those lyrics to be 0. Otherwise, count the number
# of words either delimited by spaces or by new line characters.
def count_words(lyrics:str) -> int:
    if type(lyrics) != str:
        return 0
    if len(lyrics) == 0:
        return 0
    return len(re.split("\n| ", lyrics))


# n_words calculation
data["n_words"] = np.vectorize(count_words)(data["lyrics"])

# Calculate a words per minute (wpm)
data["duration_min"] = data["duration_ms"] / 60000
# Data look normally distributed with respect to duration_min
# mean = 3.631, median = 3.560, std = 0.899
data["duration_min"].describe()
plt.hist(data["duration_min"], bins=30)
plt.show()

# Since the song duration is ~N(3.631, 0.899), we can calculate
# words per minute (wpm) as follows:
data["wpm"] = data["n_words"]/(data["duration_min"])

# Subset to just the songs that do have lyrics
data_with_lyrics = data[data["n_words"] > 0]

# Large wpm are could be indicative of incorrect lyrics being found
# using Genius' API. Based on cursory glance, usually the incorrect lyrics
# that Genius finds are playlists with a bunch unrelated song titles and artists
# or url links.

# Because of large values present in the data with respect to wpm, 
# bell curve normalization likely isn't a great choice.
# Instead, boxplot the wpm and see where there are outliers

# Box plot covering 1.5*IQR (default) for songs that do have lyrics
box_plot = plt.boxplot(data_with_lyrics["wpm"])
plt.show()

# Lower whisker and upper whisker based on n_words
wpm_lower_whisker = box_plot["whiskers"][0].get_data()[1][1]
wpm_upper_whisker = box_plot["whiskers"][1].get_data()[1][1]
high_wpm_songs = data_with_lyrics[
                        data_with_lyrics["wpm"] > wpm_upper_whisker]

# Some of the identified songs might have been falsely identified.
# The .describe() method for the wpm column shows that there is
# still a major skew even within the catchment area of the outliers 
# from earlier.
box_plot = plt.boxplot(high_wpm_songs["wpm"])
plt.show()

# Check the lyrcs of the songs whose wpm is 
# at or above the lower whisker but strictly below the
# 25th percentile of the wpm boxplot.
high_wpm_lower_whisker = box_plot["whiskers"][0].get_data()[1][1]
high_wpm_25_percentile = box_plot["boxes"][0].get_data()[1][1]

# Inspect these songs to see if they are false positives:
inspection = high_wpm_songs[
                 (high_wpm_songs["wpm"] >= high_wpm_lower_whisker) &
                    (high_wpm_songs["wpm"] < high_wpm_25_percentile)]

# The summary stats of wpm are ~N(279.966, 30.852) for these songs
inspection["wpm"].describe()

# Check the lyrics
inspection["lyrics"].head()

# Four scenarios:
# 1. The song is a playlist with a bunch of unrelated songs
# 2. The song is a url link
# 3. The song is a song that is in another language (ex: Korean)
# but has an english translation and transliteration
# 4. The song is a song that is more like rap than r&b (rap will have high
# wpm, r&b will have lower wpm)

# Blanket removal of all songs that are present in the 
# high_wpm_songs dataframe from the dataframe

data = data[~data.index.isin(high_wpm_songs.index)]
data_with_lyrics = data_with_lyrics[~data_with_lyrics.index.isin(high_wpm_songs.index)]
data_with_lyrics["wpm"].describe()
# Mean: 110.015, Median: 107.122, Std: 41.587
# wpm is now more normally distributed ~N(110.015, 41.587).
plt.hist(data_with_lyrics["wpm"], bins=30)
plt.show()

# Another boxplot, but this time, let the whisks be 1*IQR
# This is to check for songs that have suspiciously low wpm
box_plot = plt.boxplot(data_with_lyrics["wpm"], whis=1)
plt.show()

# Lower whisker based on wpm
wpm_lower_whisker = box_plot["whiskers"][0].get_data()[1][1]
low_wpm_songs = data_with_lyrics[data_with_lyrics["wpm"] < wpm_lower_whisker]

# These songs also have incorrect lyrics (ie: url links or playlist songs
# just like the high wpm songs)
# They are in a language that isn't English (this time, Chinese and Korean)
# Or, if the lyrics were correct, the song wasn't r&b.
# Dropping these also from the dataframe.
data_with_lyrics = data_with_lyrics[
                      ~data_with_lyrics.index.isin(low_wpm_songs.index)]

# Data still aren't quite clean. One more pass
# Inspect songs in this dataframe whose wpm is an flier in the boxplot
# using the default whis=1.5
box_plot = plt.boxplot(data_with_lyrics["wpm"])
plt.show()

# Upper whisker
wpm_upper_whisker = box_plot["whiskers"][1].get_data()[1][1]
double_check = data_with_lyrics[data_with_lyrics["wpm"] > wpm_upper_whisker]

# Remove these too
data_with_lyrics = data_with_lyrics[
                       ~data_with_lyrics.index.isin(double_check.index)]

# Number of songs removed due to:
# No lyrics found by Genius: 45
# High wpm: 124
# Low wpm: 20

# Save this dataframe for further cleaning later.
data_with_lyrics.to_csv("data_clean.csv")