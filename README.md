# Recommender
Some model python code for testing various data mining algorithms

cosine.py - Builds a recommender based on an item-item model based collaborative filtering algorithm. Each item can only be 
rated "1" for went there or "0" for did not go there. This ensure that every location has a rating, which helps alleviate the
problem of data sparsity that plaugues many recommendation systems.

mov.csv - A hypothetical dataset of people rating movies. Since this data is completely fabricated, the tests tell us nothing
about the predicative strength of the algorithm. However, it does tell us whether the code meets some other important 
criteria

sparse.csv - mov.csv with a lot of data entries removed. The performance of cosine.py on this dataset is the best indication
we have that our code solves some of the data sparsity problems a lot of recommendation systems have.

content.py - Builds a recommender based on content based filtering. Each item is rated on a scale in whatever qualities are
chosen and a table of distances is built based on these. The specific distance formula used can be tweaked. content.py also 
features a cross-recomendation class that gives recommendations across datasets

chicago.csv - A dataset where I went and manually rated various locations in Chicago in a variety of criteria

nyc.csv - Same as chicago.csv, but for New York City

The content.py algorithm gives intuitively sensible predictions based on the very quickly put together datasets that I
tested on.

For the future, we want to take these distance algorithms and try to combine them with more "context aware" systems that
consider all kinds of data before making a recommendation.
