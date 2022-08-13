# Here are the models that were attempted.  Only one will come out as the winner.

# Creating the baseline model.
import pandas as pd
import numpy as np
import math as m

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
# import matplotlib.pyplot as plt
from utils import get_mae, get_mse, get_rmse, strip_punctuation, calculate_tfidf
from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import LinearRegression
from statsmodels.multivariate.manova import MANOVA
# import statsmodels.api as sm
# import statsmodels.formula.api as smf
# import statsmodels.tools.eval_measures as smt

# Prevent (excessive) scientific notation
np.set_printoptions(suppress=True,
   formatter={'float_kind':'{:.4f}'.format})

# Bring in the training data
X = pd.read_csv('data/05_x_train.csv')
# Convert the year column to int, adjust so that 2013 is year 0.
X['year'] = X['year'].astype(int) - 2013
# Keep only the X columns that are not of type str
# X = X.select_dtypes(exclude=['object'])
Y = pd.read_csv("data/05_y_train.csv")
data = pd.concat([Y, X], axis=1)

def baseline_guess_one_half(Y, average_across_responses = False):
    Y_true = np.array(Y.copy())
    
    # There are 7 response values, all of them range strictly between 0 and 1
    # when they are untransformed.
    # For the values that are bound [0,1] guess 0.5.
    # For the log transformed values, guess log(0.5) = -log(2).

    Y_pred = np.matrix([0.5, 0.5, 0.5, 
                        -m.log(2), -m.log(2), -m.log(2), 0.5] * len(Y_true), 
                        dtype = np.float64).reshape(len(Y_true), 7)

    mae = get_mae(Y_true, Y_pred, average_across_responses)
    mse = get_mse(Y_true, Y_pred, average_across_responses) 
    rmse = get_rmse(Y_true, Y_pred, average_across_responses)
    return mae, mse, rmse

def baseline_guess_mean(Y, average_across_responses = False):
    Y_true = np.array(Y.copy())
    
    # There are 7 response values
    # Blindly guess the mean of each.
    # Technically, this is ``cheating`` as you won't know the mean of the 
    # validation and test sets beforehand.
    Y_pred = np.matrix(
            [np.mean(Y_true, axis=0)] * len(Y_true)
            ).reshape(len(Y_true), 7)

    mae = get_mae(Y_true, Y_pred, average_across_responses)
    mse = get_mse(Y_true, Y_pred, average_across_responses) 
    rmse = get_rmse(Y_true, Y_pred, average_across_responses)
    return mae, mse, rmse


baseline_mae, _, baseline_rmse = baseline_guess_one_half(Y)
avg_baseline_mae, _, avg_baseline_rmse = baseline_guess_one_half(Y, True)

mean_guess_baseline_mae, _, mean_guess_baseline_rmse = baseline_guess_mean(Y)
avg_mean_guess_baseline_mae, _, avg_mean_guess_baseline_rmse = baseline_guess_mean(Y, True) 

# Just throw the predictors in blindly and see what happens
dumb_reg = MultiOutputRegressor(LinearRegression()).fit(X, Y)
dumb_preds = dumb_reg.predict(X)

dumb_mae = get_mae(Y, dumb_preds)
dumb_rmse = get_rmse(Y, dumb_preds)
avg_dumb_mae = get_mae(Y, dumb_preds, average_across_responses = True)
avg_dumb_rmse = get_rmse(Y, dumb_preds, average_across_responses = True)

# Print the results
print(f" Baseline MAE: {baseline_mae}, Avg: {avg_baseline_mae}\n" + 
      f" Mean Guess MAE: {mean_guess_baseline_mae}, Avg: {avg_mean_guess_baseline_mae}\n" +
      f" Dumb Reg MAE: {dumb_mae}, Avg: {avg_dumb_mae}\n\n" + 
      f" Baseline RMSE: {baseline_rmse}, Avg: {avg_baseline_rmse}\n" + 
      f" Mean Guess RMSE: {mean_guess_baseline_rmse}, Avg: {avg_mean_guess_baseline_rmse}\n" + 
      f" Dumb Reg RMSE: {dumb_rmse}, Avg: {avg_dumb_rmse}")


def with_tfidf_vectors(X, Y, scaling = True):
    lyrics = strip_punctuation(X["lyrics"])
    _, tfidf_vectors, _ = calculate_tfidf(lyrics)
    tfidf_vectors = pd.DataFrame(tfidf_vectors)
    # Ragged array shape.  Keep first 100 columns, fill NaNs with 0.
    tfidf_vectors = tfidf_vectors.iloc[:, :100].fillna(0)
    # Name the columns
    tfidf_vectors.columns = [f"tfidf_{i}" for i in range(100)]

    # Add back in the other data columns
    X = pd.concat([X.select_dtypes(exclude=['object']), tfidf_vectors], axis=1)
    # Model
    # Each estimator is stored under the MOR's estimators attribute. ie:
    # model.estimators_[idx].named_steps["linearregression"].coef_
    # to access that linear regression model's coefficients.
    model = MultiOutputRegressor(
              make_pipeline(StandardScaler(with_mean=scaling, 
                              with_std=scaling), 
                LinearRegression())).fit(X, Y)
    preds = model.predict(X)

    mae = get_mae(Y, preds)
    rmse = get_rmse(Y, preds)
    avg_mae = get_mae(Y, preds, average_across_responses = True)
    avg_rmse = get_rmse(Y, preds, average_across_responses = True)
    return model, preds, mae, rmse, avg_mae, avg_rmse 

