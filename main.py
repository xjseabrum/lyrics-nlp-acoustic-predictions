# This is the main entry point for the program.
from setup import *

def main():
    data = create_or_load_data()
    data = add_genius_data(dataset = data)
    data = clean_data(dataset = data)
    data = subset_to_rnb(dataset = data)
    return data

if __name__ == "__main__":
    data = main()