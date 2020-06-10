from kmeans import *
import sys
import matplotlib.pyplot as plt
from nn import *
plt.ion()
from pcaimg import *

def mogEM(x, K, iters, minVary=0, kmean_iters = None, stop_graph = True, output_result = True):
  """
  Fits a Mixture of K Gaussians on x.
  Inputs:
    x: data with one data vector in each column.
    K: Number of Gaussians.
    iters: Number of EM iterations.
    minVary: minimum variance of each Gaussian.

  Returns:
    p : probabilities of clusters.
    mu = mean of the clusters, one in each column.
    vary = variances for the cth cluster, one in each column.
    logProbX = log-probability of data after every iteration.
  """
  N, T = x.shape

  # Initialize the parameters
  randConst = 1
  p = randConst + np.random.rand(K, 1)
  p = p / np.sum(p)
  mn = np.mean(x, axis=1).reshape(-1, 1)
  vr = np.var(x, axis=1).reshape(-1, 1)
 
  # Change the initializaiton with Kmeans here
  #--------------------  Add you code here --------------------
  if not kmean_iters:
    mu = mn + np.random.randn(N, K) * (np.sqrt(vr) / randConst)
  else:
    mu = KMeans(x, K, kmean_iters)
  
  #------------------------------------------------------------  
  vary = vr * np.ones((1, K)) * 2
  vary = (vary >= minVary) * vary + (vary < minVary) * minVary

  logProbX = np.zeros((iters, 1))

  # Do iters iterations of EM
  for i in xrange(iters):
    # Do the E step
    respTot = np.zeros((K, 1))
    respX = np.zeros((N, K))
    respDist = np.zeros((N, K))
    logProb = np.zeros((1, T))
    ivary = 1 / vary
    logNorm = np.log(p) - 0.5 * N * np.log(2 * np.pi) - 0.5 * np.sum(np.log(vary), axis=0).reshape(-1, 1)
    logPcAndx = np.zeros((K, T))
    for k in xrange(K):
      dis = (x - mu[:,k].reshape(-1, 1))**2
      logPcAndx[k, :] = logNorm[k] - 0.5 * np.sum(ivary[:,k].reshape(-1, 1) * dis, axis=0)
    
    mxi = np.argmax(logPcAndx, axis=1).reshape(1, -1) 
    mx = np.max(logPcAndx, axis=0).reshape(1, -1)
    PcAndx = np.exp(logPcAndx - mx)
    Px = np.sum(PcAndx, axis=0).reshape(1, -1)
    PcGivenx = PcAndx / Px
    logProb = np.log(Px) + mx
    logProbX[i] = np.sum(logProb)
    if output_result:
      print 'Iter %d logProb %.5f' % (i, logProbX[i])

    # Plot log prob of data
    plt.figure(1);
    plt.clf()
    plt.plot(np.arange(i), logProbX[:i], 'r-')
    plt.title('Log-probability of data versus # iterations of EM')
    plt.xlabel('Iterations of EM')
    plt.ylabel('log P(D)');
    plt.draw()
    ##raw_input('Press Enter to continue.')

    respTot = np.mean(PcGivenx, axis=1).reshape(-1, 1)
    respX = np.zeros((N, K))
    respDist = np.zeros((N,K))
    for k in xrange(K):
      respX[:, k] = np.mean(x * PcGivenx[k,:].reshape(1, -1), axis=1)
      respDist[:, k] = np.mean((x - mu[:,k].reshape(-1, 1))**2 * PcGivenx[k,:].reshape(1, -1), axis=1)

    # Do the M step
    p = respTot
    mu = respX / respTot.T
    vary = respDist / respTot.T
    vary = (vary >= minVary) * vary + (vary < minVary) * minVary
  
  if stop_graph:
    raw_input('Press Enter to continue.')
  
  return p, mu, vary, logProbX

def mogLogProb(p, mu, vary, x):
  """Computes logprob of each data vector in x under the MoG model specified by p, mu and vary."""
  K = p.shape[0]
  N, T = x.shape
  ivary = 1 / vary
  logProb = np.zeros(T)
  for t in xrange(T):
    # Compute log P(c)p(x|c) and then log p(x)
    logPcAndx = np.log(p) - 0.5 * N * np.log(2 * np.pi) \
        - 0.5 * np.sum(np.log(vary), axis=0).reshape(-1, 1) \
        - 0.5 * np.sum(ivary * (x[:, t].reshape(-1, 1) - mu)**2, axis=0).reshape(-1, 1)

    mx = np.max(logPcAndx, axis=0)
    logProb[t] = np.log(np.sum(np.exp(logPcAndx - mx))) + mx
  return logProb

def q2():
  temp = True
  while temp:
    iters = raw_input("Number of iterations: ")
    K = 2
    min_var = 0.01
    inputs_train2, inputs_valid2, inputs_test2, target_train2, target_valid2, target_test2 = LoadData('digits.npz',
                                                                                                      True, False)
    inputs_train3, inputs_valid3, inputs_test3, target_train3, target_valid3, target_test3 = LoadData('digits.npz',
                                                                                                      False, True)

    if(iters.isdigit()):
      iters = int(iters)
    else:
      iters = 0

    run_class = raw_input("What class do you want to run? (2,3)")
    if run_class == '2':
      print(inputs_train2.shape)
      p2, mu2, vary2, logProbX2 = mogEM(inputs_train2, K, iters, min_var)
      ShowMeans(mu2)
      ShowMeans(vary2)
      print(mu2.shape)
      print(p2)

    if run_class == '3':
      p3, mu3, vary3, logProbX3 = mogEM(inputs_train3, K, iters, min_var)
      ShowMeans(mu3)
      ShowMeans(vary3)
      print(p3)
    q = raw_input("Do you want to quit? (Y,N)\n")
    if q == 'Y' or q == 'y':
      temp = False


def q3():
  temp = True
  iters = raw_input("Number of iterations: ")
  minVary = 0.01
  K = 20
  kmean_iters = 5
  inputs_train, inputs_valid, inputs_test, target_train, target_valid, target_test = LoadData('digits.npz')
  if(iters.isdigit()):
    iters = int(iters)
  else:
    iters = 10
  while temp:
    run_10 = raw_input("Run multi-time? ")
    if run_10 == 'Y' or run_10 == 'y':
      logProbX_all = np.zeros((20, 1))
      iters = 20
      for i in range (20):
        p, mu, vary, logProbX = mogEM(inputs_train, K, iters, minVary, kmean_iters, False, False)
        logProbX_all += logProbX
      plt.figure(1)
      raw_input('Press Enter to continue.')
      plt.clf()
      plt.plot(np.arange(20), logProbX_all[:20]/20.0, 'r-')
      plt.title('Average Log-probability of data versus # iterations of EM')
      plt.xlabel('Iterations of EM')
      plt.ylabel('avg log P(D)');
      plt.draw()
      raw_input('Press Enter to continue.')
      logProbX_all = np.zeros((20, 1))
      for i in range (20):
        p, mu, vary, logProbX = mogEM(inputs_train, K, iters, minVary, None, False, False)
        logProbX_all += logProbX
      plt.figure(1)
      raw_input('Press Enter to continue.')
      plt.clf()
      plt.plot(np.arange(20), logProbX_all[:20]/20.0, 'r-')
      plt.title('Average Log-probability of data versus # iterations of EM')
      plt.xlabel('Iterations of EM')
      plt.ylabel('avg log P(D)');
      plt.draw()
      raw_input('Press Enter to continue.')
    
    # Train a MoG model with 20 components on all 600 training
    # vectors, with both original initialization and kmeans initialization.
    #------------------- Add your code here ---------------------
    else:
      p, mu, vary, logProbX = mogEM(inputs_train, K, iters, minVary, kmean_iters)
      p, mu, vary, logProbX = mogEM(inputs_train, K, iters, minVary)
      raw_input('Press Enter to continue.')
    
    q = raw_input("Do you want to quit? (Y,N)\n")
    if q == 'Y' or q == 'y':
      temp = False

def q4():
  run = raw_input("Number of runs: ")
  if(run.isdigit()):
    run = int(run)
  else:
    run = 1
  
  iters = 10
  minVary = 0.01
  errorTrain = np.zeros(4)
  errorTest = np.zeros(4)
  errorValidation = np.zeros(4)
  kmean_iters = 5
  #print(errorTrain)
  numComponents = np.array([2, 5, 15, 50])#I changed this list's values
  T = numComponents.shape[0]  
  inputs_train, inputs_valid, inputs_test, target_train, target_valid, target_test = LoadData('digits.npz')
  train2, valid2, test2, target_train, target_valid, target_test = LoadData('digits.npz', True, False)
  train3, valid3, test3, target_train, target_valid, target_test = LoadData('digits.npz', False, True)

  for i in range(run):
    for t in range(T): 
      K = numComponents[t]
      #print("For K = ", K)
      counter = 0
      # Train a MoG model with K components for digit 2
      #-------------------- Add your code here --------------------------------
      p2, mu2, vary2, logProbX2 = mogEM(train2, K, iters, minVary, kmean_iters, False, False)

      
      # Train a MoG model with K components for digit 3
      #-------------------- Add your code here --------------------------------
      p3, mu3, vary3, logProbX3 = mogEM(train3, K, iters, minVary, kmean_iters, False, False)

      
      # Caculate the probability P(d=1|x) and P(d=2|x),
      # classify examples, and compute error rate
      # Hints: you may want to use mogLogProb function
      #-------------------- Add your code here --------------------------------
      # it is given in the assignment that train2 and train3 each contain 300
      # training examples of handwritten 2's and 3's, respectively. Therefore,
      # p(d=1) = p(d=2) = 0.5
      # p(d|x) = p(x|d)p(d)/p(x)
      # p(x) = p(x|d=1)p(d=1) + p(x|d=2)p(d=2)

      # p(x|d=1)
      p_x_given_d_1 = mogLogProb(p2, mu2, vary2, train2)

      # p(x|d=2)
      p_x_given_d_2 = mogLogProb(p3, mu3, vary3, train2)

      #p_x = p_x_given_d_1 * 0.5 + p_x_given_d_2 * 0.5

      #p(d=1|x) = p(x|d=1) * p(d=1) / (p(x|d=1)p(d=1) + p(x|d=2)p(d=2))
      #p_d_1_x = p_x_given_d_1 * 0.5 / p_x

      #p_d_2_x = p_x_given_d_1 * 0.5 / p_x

      for i in xrange(p_x_given_d_1.shape[0]):
        if p_x_given_d_1[i] < p_x_given_d_2[i]:
          counter += 1

      p_x_given_d_1 = mogLogProb(p2, mu2, vary2, train3)
      p_x_given_d_2 = mogLogProb(p3, mu3, vary3, train3)

      p_x = (p_x_given_d_1 + p_x_given_d_2) * 0.5

      for i in xrange(p_x_given_d_1.shape[0]):
        if p_x_given_d_1[i] > p_x_given_d_2[i]:
          counter += 1

      N2, T2 = train2.shape
      N3, T3 = train3.shape
      errorTrain[t] += counter / float(T2+T3)

      counter = 0

      p_x_given_d_1 = mogLogProb(p2, mu2, vary2, valid2)
      p_x_given_d_2 = mogLogProb(p3, mu3, vary3, valid2)

      for i in xrange(p_x_given_d_1.shape[0]):
        if p_x_given_d_1[i] < p_x_given_d_2[i]:
          counter += 1

      p_x_given_d_1 = mogLogProb(p2, mu2, vary2, valid3)
      p_x_given_d_2 = mogLogProb(p3, mu3, vary3, valid3)
      for i in xrange(p_x_given_d_1.shape[0]):
        if p_x_given_d_1[i] > p_x_given_d_2[i]:
          counter += 1
      N2, T2 = valid2.shape
      N3, T3 = valid3.shape
      errorValidation[t] += counter / float(T2+T3)

      counter = 0

      p_x_given_d_1 = mogLogProb(p2, mu2, vary2, test2)
      p_x_given_d_2 = mogLogProb(p3, mu3, vary3, test2)

      for i in xrange(p_x_given_d_1.shape[0]):
        if p_x_given_d_1[i] < p_x_given_d_2[i]:
          counter += 1

      p_x_given_d_1 = mogLogProb(p2, mu2, vary2, test3)
      p_x_given_d_2 = mogLogProb(p3, mu3, vary3, test3)
      for i in xrange(p_x_given_d_1.shape[0]):
        if p_x_given_d_1[i] > p_x_given_d_2[i]:
          counter += 1
      N2, T2 = test2.shape
      N3, T3 = test3.shape
      errorTest[t] += counter / float(T2+T3)
    
  # Plot the error rate
  plt.clf()
  #-------------------- Add your code here --------------------------------
  line1, = plt.plot(numComponents, errorTrain / float(run), 'go-', label = 'Train')
  line2, = plt.plot(numComponents, errorValidation / float(run), 'r*-', label = 'Valid')
  line3, = plt.plot(numComponents, errorTest / float(run), 'b+-', label = 'Test')
  plt.title('Error rate vs k')
  plt.xlabel('k')
  plt.ylabel('Error rate');
  plt.legend()
  plt.draw()
  raw_input('Press Enter to continue.')

def q5():
  # Choose the best mixture of Gaussian classifier you have, compare this
  # mixture of Gaussian classifier with the neural network you implemented in
  # the last assignment.

  # Train neural network classifier. The number of hidden units should be
  # equal to the number of mixture components.

  # Show the error rate comparison.
  #-------------------- Add your code here --------------------------------
  num_hiddens = 15
  eps = 0.1
  momentum = 0.0
  num_epochs = 1000
  W1, W2, b1, b2, train_error, valid_error = TrainNN(num_hiddens, eps, momentum, num_epochs)

  for i in range(0,num_hiddens,5):
    ShowMeans(W1.T[i:i+5].T)

  inputs_train, inputs_valid, inputs_test, target_train, target_valid, target_test = LoadData('digits.npz')
  train2, valid2, test2, target_train, target_valid, target_test = LoadData('digits.npz', True, False)
  train3, valid3, test3, target_train, target_valid, target_test = LoadData('digits.npz', False, True)
  
  p, mu, vary, logProbX = mogEM(train2, num_hiddens, 50, 0.01, 5, False, True)
  for i in range(0,num_hiddens,5):
    ShowMeans(mu.T[i:i+5].T)

  raw_input('Press Enter to continue.')

  p, mu, vary, logProbX = mogEM(train3, num_hiddens, 50, 0.01, 5, False, True)
  for i in range(0,num_hiddens,5):
    ShowMeans(mu.T[i:i+5].T)

  raw_input('Press Enter to continue.')

def q6():
  # Apply the PCA algorithm to the digit images. 
  # Plot the (sorted) eigenvalues and visualize the top-3 eigenvectors. 
  #-------------------- Add your code here --------------------------------
  K = 256
  inputs_train, inputs_valid, inputs_test, target_train, target_valid, target_test = LoadData('digits.npz')
  
  w, v, mean, projX = pcaimg(inputs_train, K)
  error = []
  w = w[::-1]
  temp_v = np.fliplr(v)
  ShowEigenVectors(temp_v.T[0:3].T)
  ShowMeans(mean)

  plt.clf()

  plt.plot(range(w.shape[0]), w, 'b-', label = 'Eigen values')
  plt.title('Eigen Values')
  plt.xlabel('m')
  plt.ylabel('eigen values');
  plt.legend()
  plt.draw()
  raw_input('Press Enter to continue.')

  # Conduct NN-based classification using PCA with different numbers of
  # eigenvectors. Then show the error rate comparison.
  #-------------------- Add your code here --------------------------------
  L = [2,5,10,20]
  for k in L:
    w, v, mean, projX = pcaimg(inputs_train, k)
    projValid = v.T.dot(inputs_valid - mean)
    labels = run_knn(1, projX.T, target_train.T, projValid.T)
    print(error_rate(labels, target_valid))
    error.append(error_rate(labels, target_valid))

  plt.clf()
  #-------------------- Add your code here --------------------------------
  plt.plot(L, error, 'go-', label = 'Valid error')
  plt.title('Error rate vs m')
  plt.xlabel('m')
  plt.ylabel('Error rate');
  plt.legend()
  plt.draw()

  raw_input('Press Enter to continue.')

  error = []

  for k in range(1, 30):
    w, v, mean, projX = pcaimg(inputs_train, k)
    projValid = v.T.dot(inputs_valid - mean)
    labels = run_knn(1, projX.T, target_train.T, projValid.T)
    print "error_rate for k =" + str(k) + ": " + str(error_rate(labels, target_valid))
    error.append(error_rate(labels, target_valid))

  plt.clf()
  #-------------------- Add your code here --------------------------------
  plt.plot(range(1, 30), error, 'go-', label = 'Valid error')
  plt.title('Error rate vs m')
  plt.xlabel('m')
  plt.ylabel('Error rate');
  plt.legend()
  plt.draw()

  raw_input('Press Enter to continue.')

def error_rate(predict_targets, targets):
  misclassified = 0

  for i in range(len(targets.T)):
    if predict_targets[i][0] != targets.T[i]:
      misclassified = misclassified + 1
  return float(misclassified) / float(len(targets.T))


def run_knn(k, train_data, train_labels, valid_data):

    dist = distmat(valid_data.T, train_data.T)
    nearest = np.argsort(dist, axis=1)[:,:k]

    train_labels = train_labels.reshape(-1)
    valid_labels = train_labels[nearest]

    # note this only works for binary labels
    valid_labels = (np.mean(valid_labels, axis=1) >= 0.5).astype(np.int)
    valid_labels = valid_labels.reshape(-1,1)

    return valid_labels

if __name__ == '__main__':

  run = True
  while (run):
    x = raw_input("Which part do you want to run? (2,3,4,5,6)\n")
    if (x=='2'):
      q2()
    elif (x=='3'):
      q3()
    elif (x=='4'):
      q4()
    elif (x=='5'):
      q5()
    elif (x=='6'):
      q6()
    else:
      q = raw_input("Do you want to quit? (Y,N)\n")
      if q == 'Y' or q == 'y':
        run = False
  
