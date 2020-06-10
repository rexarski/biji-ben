function [ out ] = estimate_(gamma,rho,trainx,trainy)
MSE = zeros(1,10);
for k = 1:10
    [x_test,x_train,y_test,y_train] = split(trainx,trainy,k);
    C = zeros(225,225);
    for i=1:225
        for j = i:225
        C(i,j) = K2(gamma,rho,x_train(i,:),x_train(j,:)) ;
        C(j,i) = C(i,j);
        end   
    end
    C = C + eye(225);
    
    predict = zeros(1,25);
    for i = 1:25
        t = zeros(1,225);
        for j = 1:225
            t(j) = K2(gamma,rho,x_train(j,:),x_test(i,:)) ;
        end
         predict(i) = t*pinv(C)*y_train;
    end
    
    MSE(k) = sum((transpose(y_test) - predict).^2);
      
end
out = sum(MSE);



end

