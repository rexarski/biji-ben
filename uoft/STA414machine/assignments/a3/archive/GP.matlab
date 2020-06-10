function [SSE_test, SSE_test_mean] = GP(gamma_opt, roh_opt, train1x, train1y,testx, testy)
% gaussian process model
beta = 1;
theta = 100^2;
quadretic_form = ones(length(train1x));
for j = 1:length(train1x)
    for i = 1:length(train1x)
        quadretic_form(i,j) = sum((train1x(j,:) - train1x(i,:)).^2); % this migth be rigth..
    end
end
K = theta*ones(length(train1x)) + (gamma_opt^2)*exp((-1)*(roh_opt^2)*quadretic_form);
C = K + (beta^(-1))*eye(length(K));
C = inv(C);
parameters = ones(length(train1x), 2);
for i = 1:length(testy)
    quadretic_form = ones(length(train1y),1);
    for l = 1:length(train1y)
        quadretic_form(l) = sum((train1x(l,:) - testx(i,:)).^2); % this migth be rigth..
    end
    k = theta*ones(length(train1y),1) + (gamma_opt^2)*exp((-1)*(roh_opt^2)*quadretic_form);
    %c  = (100^2)*test_x(i,:)*test_x(i,:)' + beta^(-1);
    mu = transpose(k)*C*train1y;
    parameters(i,1) = mu;
    parameters(i,2) = 1;
end
SSE_test = 0; % SSE for test
for i = 1:length(testy)
    se = (testy(i) - parameters(i,1))^2;
    SSE_test = SSE_test + se;
end
SSE_test_mean = SSE_test/(length(testy));