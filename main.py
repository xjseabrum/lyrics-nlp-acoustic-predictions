# This is the main entry point for the program.

from setup import create_or_load_data, add_genius_data, clean_data

def main():
    data = create_or_load_data()
    data = add_genius_data(dataset = data)
    data = clean_data(dataset = data)
    return data

if __name__ == "__main__":
    data = main()