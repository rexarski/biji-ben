function [SSE_test, SSE_test_mean] = GPLC(par, train1x, train1y,testx, testy)
if par == 0 %divide covariates 1 to 7 by 10
    train1x(:,1:7) = (1/10)*train1x(:,1:7);
    testx(:,1:7) = (1/10)*testx(:,1:7);
end
K = (100^2)*(train1x*transpose(train1x));
beta = 1;
C = K + (beta^(-1))*eye(length(K));
C = inv(C);
size(C)
parameters = ones(length(testx), 2); %[mu_i, sigma_i]
for i = 1:length(testy)
    k = (100^2)*train1x*transpose(testx(i,:)); 
    c  = (100^2)*testx(i,:)*testx(i,:)' + beta^(-1);  
    mu = transpose(k)*C*train1y;
    sigma = c - transpose(k)*C*k;
    parameters(i,1) = mu;
    parameters(i,2) = sigma;
end
SSE_test = 0; % SSE for the test set using the optimal weigths
for i = 1:length(testy)
    se = (testy(i) - parameters(i,1))^2;
    SSE_test = SSE_test + se;
end
SSE_test_mean = SSE_test/(length(testy));