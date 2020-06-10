from util import *
import scipy.linalg as lin
import matplotlib.pyplot as plt
plt.ion()

def pcaimg(X, k):
  """
  PCA matrix X to k dimensions.
  Inputs:
    X : Each column of X contains a data vector.
    k : Number of dimensions to reduce to.
  Returns:
    v : The eigenvectors. Each column of v is an eigenvector.
    mean : mean of X.
    projX : X projected down to k dimensions.
  """
  xdim, ndata = X.shape
  mean = np.mean(X, axis=1).reshape(-1, 1)
  X = X - mean
  cov = np.dot(X, X.T) / ndata

  w, v = lin.eigh(cov, eigvals=(xdim - k, xdim - 1))
  # w contains top k eigenvalues in increasing order of magnitude.
  # v contains the eigenvectors corresponding to the top k eigenvalues.

  projX = np.dot(v.T, X)
  return w, v, mean, projX

def ShowEigenVectors(v):
  """Displays the eigenvectors as images in decreasing order of eigen value."""
  plt.figure(1)
  plt.clf()
  for i in xrange(v.shape[1]):
    plt.subplot(1, v.shape[1], i+1)
    plt.imshow(v[:, v.shape[1] - i - 1].reshape(16, 16).T, cmap=plt.cm.gray)
  plt.draw()
  raw_input('Press Enter.')

def main():
  K = 5  # Number of dimensions to PCA down to.
  inputs_train, inputs_valid, inputs_test, target_train, target_valid, target_test = LoadData('digits.npz')
  v, mean, projX = pcaimg(inputs_train, K)
  ShowEigenVectors(v)

if __name__ == '__main__':
  main()
