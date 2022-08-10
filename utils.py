# Utility functions for the project

# Speeding up API calls
# See https://blog.devgenius.io/best-way-to-speed-up-a-bulk-of-http-requests-in-python-4ec75badabed#df95

# import asyncio
# import aiohttp
# from aiolimiter import AsyncLimiter
# limiter = AsyncLimiter(1, 0.125)

import re
import numpy as np
from scipy.stats import skew, kurtosis

# If Genius didn't find lyrics/rejected the search, it returns a None type
# Setting the length of those lyrics to be 0. Otherwise, count the number
# of words either delimited by spaces or by new line characters.

def count_words(lyrics:str) -> int:
    if type(lyrics) != str:
        return 0
    if len(lyrics) == 0:
        return 0
    return len(re.split("\n| ", lyrics))

def fd_bins(data_column):
    # Using the Freedman-Diaconis rule to determine the number of bins
    # https://en.wikipedia.org/wiki/Freedman%E2%80%93Diaconis_rule
    iqr = np.subtract(*np.percentile(data_column, [75, 25]))
    n_obs = len(data_column)
    h = (2 * iqr * (n_obs**(-1/3)))
    max_ = max(data_column)
    min_ = min(data_column)
    return int(((max_ - min_)/h) // 1)

def get_skew(data_points):
    return skew(data_points, bias = False)

def get_fisher_kurtosis(data_points):
    return kurtosis(data_points, bias = False, fisher = True)

def epsilon_log(column, epsilon = 1e-6):
    # Adds small value epsilon before evaluating the log
    # so as to prevent -Inf in evaluation.  Set value to 
    # 1e-6 or lower.
    value = column + epsilon
    return m.log(value)