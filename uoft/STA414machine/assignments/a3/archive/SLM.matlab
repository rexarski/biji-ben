function [SSE_test, SSE_test_mean] = SLM(par, train1x, train1y,testx, testy)
if par == 0 %divide covariates 1 to 7 by 10
    train1x(:,1:7) = (1/10)*train1x(:,1:7);
    testx(:,1:7) = (1/10)*testx(:,1:7);

end
w_opt = ones(9,1);
X = [ones(length(train1x),1) train1x]; % X is the desing matrix for the train set
w_opt = inv(transpose(X)*X)*transpose(X)*train1y; %optimat weigths
X_test = [ones(length(testx),1) testx]; % design matrix for the test set
SSE_test = 0; % SSE for the test set using the optimal weigths
for i = 1:length(testy)
    se = (testy(i) - X_test(i,:)*w_opt)^2;
    SSE_test = SSE_test + se;
end
SSE_test_mean = SSE_test/(length(testy)); 