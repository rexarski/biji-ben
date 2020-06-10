function [mean_opt, gamma_opt, roh_opt] = calcHyperparameters(train1x, train1y)
% calculates the optimal hyperparameters using cross validation
theta = 100^2;
for gamma = 0.1:0.5:10
    for roh = 0.01:0.05:1
        ASSE = crossValidation(train1x, train1y, gamma, roh, theta);  
        % ASSE = average sum of squerd error                   
        if gamma == 0.1 && roh == 0.01
            mean_opt = ASSE;
            gamma_opt = gamma;
            roh_opt = roh;
        end
        if ASSE < mean_opt
            mean_opt = ASSE;
            gamma_opt = gamma;
            roh_opt = roh;
        end
            
    end
end