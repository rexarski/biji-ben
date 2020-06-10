In this example, we look at simulated bivariate data generated from two populations - the two clusters are quite clear from the plot.  The clusters are estimated using k-means and using a bivariate normal mixture model, which is estimated using the EM algorithm as described in lecture.

I have written a very crude and inefficient R function to estimate the parameters in the mixture model using k-means clusters to generate initial values for the parameters.  Feel free to try the function out and modify it as you wish.

