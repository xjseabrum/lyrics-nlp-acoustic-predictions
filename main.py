# Ignore this file for now.
# Eventually this will be the main entry point for the program.

from setup import create_or_load_data

def main():
    data = create_or_load_data()
    data["comb"] = data["song_name"] + " ::: " + data["main_artist"]
    return data

if __name__ == "__main__":
    data = main()