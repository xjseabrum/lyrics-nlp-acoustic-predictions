# Ignore this file for now.
# Eventually this will be the main entry point for the program.

from os.path import exists
from spotify_data import gather_track_uris

def main():
    if not exists("song_data.csv"):
        gather_track_uris()

if __name__ == "__main__":
    main()