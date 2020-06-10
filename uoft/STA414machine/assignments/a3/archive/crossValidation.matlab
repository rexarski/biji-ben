function ASSE = crossValidation(train1x, train1y, gamma, roh, theta)
% cross validation of the train set by dividing the set into 10 parts 
beta = 1;
SSE_vec = ones(10,1);
for index = 1:10 % the the different cross validations cases
    [test_x, test_y, train_y, train_x] = findIntervals(index, train1x, train1y);
    quadretic_form = ones(225);
    for j = 1:225
        for i = 1:225
            quadretic_form(i,j) = sum((train_x(j,:) - train_x(i,:)).^2); % this migth be rigth..
        end
    end
    K = theta*ones(225) + (gamma^2)*exp((-1)*(roh^2)*quadretic_form);
    C = K + (beta^(-1))*eye(length(K));
    C = inv(C);
    parameters = ones(length(test_x), 2); %[mu_i, sigma_i]
    for i = 1:length(test_y)
        quadretic_form = ones(225,1);
        for l = 1:225
            quadretic_form(l) = sum((train_x(l,:) - test_x(i,:)).^2); % this migth be rigth..
        end
        k = theta*ones(225,1) + (gamma^2)*exp((-1)*(roh^2)*quadretic_form);
        %c  = (100^2)*test_x(i,:)*test_x(i,:)' + beta^(-1);
        mu = transpose(k)*c*train_y;
        parameters(i,1) = mu;
        parameters(i,2) = 1;
    end
    SSE_test = 0; % SSE for test
    for i = 1:length(test_y)
        se = (test_y(i) - parameters(i,1))^2;
        SSE_test = SSE_test + se;
    end
    SSE_test_mean = SSE_test/(length(test_y));
    SSE_vec(index)= SSE_test_mean;

end
ASSE = sum(SSE_vec)/10;
end %end of function 