function [ MSE ] = estimate_(gamma,rho)
MSE = zeros(1,10);
for k = 1:10
    [x_train,x_test,y_train,y_test] = split(trainx,trainy,k);
    C = zeros(25,25);
    for i=1:25
        for j = 1:25
        C(i,j) = K2(gamma,rho,x_train(i,:),x_test(j,:)) ;
        end   
    end
    
    
    predict = zeros(1,250-25);
    for i = 1:250-25
        t = zeros(1,25);
        for j = 1:25
            t(j) = K2(gamma,rho,x_train(j,:),x_test(i,:)) ;
        end
        predict(i) = t*(C\y_train);
    end
    
    MSE(k) = sum((transpose(y_test) - predict).^2);
      
end




end

