function [res] = lnp_x(x,t,S0,S1,mu0,mu1)
D = 64;
if t == 0;
    res  = -D/2 * log(2*pi) - log(det(S0))/2 - ((x-mu0)*inv(S0)*transpose(x-mu0))/2;
else    
    res = -D/2 * log(2*pi) - log(det(S1))/2 - ((x-mu1)*inv(S1)*transpose(x-mu1))/2;
end

end
