# You can't stay in Python forever!
# R has good stat packages that don't exist or just aren't
# quite the same as in Python.

required.packages <- c("NbClust", "dplyr")

for (package in required.packages){
    if (!(package %in% installed.packages()[, "Package"])) {
        install.packages(package)
    }
    else {
        print(paste0(package, " is already installed, loading..."))
        # library and require use non-standard eval for loading packages
        # To make this work in a loop, character.only = TRUE is needed
        require(package, character.only = TRUE)
    }
}

# Load in the data which were made originally in Python.
data <- read.csv("data/05_x_train_st_emb.csv", header = TRUE)

# If you don't like the <- syntax in R you can still just use an =.
# data = read.csv("data.csv")
# There are some fringe cases where you DON'T want to use =
# in place of <- .  This is due to the order of operator assignments in R. 
# In short, <- and -> have a higher precedence than =.

# Set up NbClust with the st_emb columns
# can do either dplyr::select or just select as it's loaded in 
# the R environment.  Being explicit isn't a bad thing. 
data.for.nb <- dplyr::select(data, contains("st_emb"))

# NbClust.  
# Docs: https://www.rdocumentation.org/packages/NbClust/versions/3.0/topics/NbClust
# Does not work with all these data due to eigenvalues for certain columns 
# approaching 0, meaning the data matrix is not invertible.
# Specifically, column R-index 556 and 757's embeddings are all 
# practically 0 (NUMe-34).
# Additionally, some of the kwarg "index" in the NbClust library 
# also prevent evaluating the entire data at once, usually because of a 
# DIV/0 error in that index's calculation (ie: Scott's index)
nb <- NbClust(data = data.for.nb[, 1:310], distance = "euclidean"
              , min.nc = 2 , max.nc = 10 
              , method = "kmeans") # Maj. Result = 2 or 3

# Doing the other parts of the dataset and 
# seeing the results.  This is a bit of a hack.
nb2 <- NbClust(data = data.for.nb[, 311:555], distance = "euclidean"
               , min.nc = 2 , max.nc = 10 
               , method = "kmeans") # Maj. Result = 3

# Exclude cols 556 and 757
nb3 <- NbClust(data = data.for.nb[, c(557:756, 758:768)]
               , distance = "euclidean", min.nc = 2
               , max.nc = 10, method = "kmeans") # Maj. Results = 4

# Majority points to 3 clusters. 