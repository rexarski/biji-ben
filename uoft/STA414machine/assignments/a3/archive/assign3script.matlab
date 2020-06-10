%% assig3scrip
testx = dlmread('testx.txt'); %read data from files
testy = dlmread('testy.txt'); 
train1x = dlmread('train1x.txt'); 
train1y = dlmread('train1y.txt');
%%
% use this to divid covarties 1 and 7 by ten
train1x(:,1) = (1/10)*train1x(:,1);
train1x(:,7) = (1/10)*train1x(:,7);
testx(:,1) = (1/10)*testx(:,1);
testx(:,7) = (1/10)*testx(:,7);
%% LLS (with intercept)
% use tic *code* toc to time things
tic
%SML = simple linear modell (with intercept)
[SSE_test, SSE_test_mean] = SLM(1, train1x, train1y,testx, testy) 
toc
%% Gaussion process with linear covariance
% GPLC = gaussian process with linear covariance
tic
[SE_test, SSE_test_mean] = GPLC(1, train1x, train1y,testx, testy)
toc
%% Gaussion process
% need to find hyperparameters gamma and roh using cross validation 
tic
[mean_opt, gamma_opt, roh_opt] = calcHyperparameters(train1x, train1y)
toc
%%
tic
[SSE_test, SSE_test_mean] = GP(gamma_opt, roh_opt, train1x, train1y,testx, testy)
toc