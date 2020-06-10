function [ out] = K2(gamma,rho,x,y)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here

out = 100^2+gamma^2*exp(-rho^2*(sum((x-y).^2)));

end

