[trainx] = textread('train1x.txt','');
[trainy] = textread('train1y.txt','');
[testx] = textread('testx.txt','');
[testy] = textread('testy.txt','');

%%%fitting a Gausian process model with linear covariance 
C = zeros(250,250);
for i=1:250
    for j = 1:250
    C(i,j) = K1(trainx(i,:),trainx(j,:)) ;
    end   
end

C = C+eye(250);

predict = zeros(1,2500);
for i = 1:length(testy)
    t = zeros(1,250);
    for j = 1:250
    t(j) = K1(trainx(j,:),testx(i,:)) ;
    end
    predict(i) = t*(C\trainy);
end

MSE_2  = sum((transpose(testy) - predict).^2)/2500;

%%% fitting Gaussian process model for non-scaling data
out = zeros(3,400);
count = 1;
for gamma = 0.1:0.5:10
    for rho = 0.01:0.05:1
        out(:,count) = [estimate_(gamma,rho,trainx,trainy);gamma;rho];
        count = count+1;
        [count, out(1,count-1),out(2,count-1),out(3,count-1)]
    end


end


dlmwrite('out1.txt',out,'\t')

index = find(out(1,:) ==min(out(1,:)));
gamma = out(2,index);
rho = out(3,index);

C = zeros(250,250);
for i=1:250
    for j = 1:250
    C(i,j) = K2(gamma,rho,trainx(i,:),trainx(j,:)) ;
    end   
end
 C = C + eye(250);
 

predict = zeros(1,2500);
for i = 1:length(testy)
    t = zeros(1,250);
    for j = 1:250
    t(j) = K2(gamma,rho,trainx(j,:),testx(i,:)) ;
    end
    predict(i) = t*(C\trainy);
end

MSE_3_a = sum((transpose(testy) - predict).^2)/2500;

%%% fitting Gaussian provess model for scaling data

trainx_ = trainx;
testx_ = testx;
trainx_(:,1) = trainx(:,1)/10 ;
trainx_(:,7) = trainx(:,7)/10;
testx_(:,1) = testx(:,1)/10 ;
testx_(:,7) = testx(:,7)/10;

out_2 = zeros(3,400);
count = 1;
for gamma = 0.1:0.5:10
    for rho = 0.01:0.05:1
        out_2(:,count) = [estimate_(gamma,rho,trainx_,trainy);gamma;rho];
        count = count+1;
        [count, out_2(1,count-1),out_2(2,count-1),out_2(3,count-1)]
    end

end
index = find(out_2(1,:) ==min(out_2(1,:)));
gamma = 4.6;
rho = 0.96;

C = zeros(250,250);
for i=1:250
    for j = 1:250
    C(i,j) = K2(gamma,rho,trainx_(i,:),trainx_(j,:)) ;
    end   
end
 C = C + eye(250);
 

predict_2 = zeros(1,2500);
for i = 1:length(testy)
    t = zeros(1,250);
    for j = 1:250
    t(j) = K2(gamma,rho,trainx_(j,:),testx_(i,:)) ;
    end
    predict_2(i) = t*(C\trainy);
end

MSE_3_b = sum((transpose(testy) - predict_2).^2)/2500;



