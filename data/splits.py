# Split into train, validation, and test sets:
#   - train: 70% of the data
#   - validation: 15% of the data
#   - test: 15% of the data

from sklearn.model_selection import train_test_split
import pandas as pd

data = pd.read_csv("data/04_rnb_selected_features.csv")

Y = data[["acousticness", "danceability", "energy", "log_instrumentalness", 
          "log_liveness", "log_speechiness", "valence"]]
X = data[["log_duration_min", "log_tempo", "wpm", "year", "n_artists", 
          "explicit", "mode", "comb", "lyrics"]]

train_size = 0.70 # ~611 observations
valid_size = 0.15 # ~131 observations
test_size = 0.15 # ~131 observations

x_train, x_test, y_train, y_test = train_test_split(X, Y, 
                                    stratify = X["year"], 
                                    test_size = test_size)

x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train,
                                    stratify = x_train["year"],
                                    test_size = (valid_size)/(train_size + valid_size))

# Save to csv
x_train.to_csv("data/05_x_train.csv", index = False)
x_valid.to_csv("data/05_x_valid.csv", index = False)
x_test.to_csv("data/05_x_test.csv", index = False)
y_train.to_csv("data/05_y_train.csv", index = False)
y_valid.to_csv("data/05_y_valid.csv", index = False)
y_test.to_csv("data/05_y_test.csv", index = False)
