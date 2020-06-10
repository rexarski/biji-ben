function [base,mean,projX] = pcaimg(X,k)
%% pca analysis of image data
%% input: X: vectorized image data
%%        k: number of eigenvectors you want to keep
%% output: base: eigenvectors
%%         mean: mean of data
%%         projX: the projected data in the low-dimensional 
%%                space.

disp('eigendecomposition...');
[xdim,ndata] = size(X);
mean = sum(X,2)/ndata;  % compute mean of data
X = X-repmat(mean,1,ndata); % substract the mean
cov = X*X'/ndata;  % form the covariance matrix

[ev,ed]=eig(cov);  %eigendecomposition
ed = diag(ed);

% Sort eigenvectors by eigenvalues
[foo,p]=sort(-ed);
ed = ed(p);
ev = ev(:,p);

% Take the top k eigenvectors
base = ev(:,1:k);

% project the data into low-dim space
projX = base'*X;
