function [res] = lnp_t(x,t,S0,S1,mu0,mu1)
res = lnp_x(x,t,S0,S1,mu0,mu1) -log(exp(lnp_x(x,0,S0,S1,mu0,mu1))+exp(lnp_x(x,1,S0,S1,mu0,mu1)));

end
