# You can't stay in Python forever!
# R has good stat packages that don't exist or just aren't
# quite the same as in Python.

require(NbClust)
library(NbClust)

# Load in the data which were made originally in Python.
data <- read.csv("data/05_x_train_st_emb.csv", header = TRUE)

# If you don't like the <- syntax in R you can still just use an =.
# data = read.csv("data.csv")
# There are some fringe cases where you DON'T want to use =
# in place of <- .  This is due to the order of operator assignments in R. 
# In short, <- and -> have a higher precedence than =.


