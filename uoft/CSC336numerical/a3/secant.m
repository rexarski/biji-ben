function res = secant(x0,x1)
format long
f0 = x0*exp(1)^(-x0/2)-exp(-1)/2;
f1 = x1*exp(1)^(-x1/2)-exp(-1)/2;
x = x1 - f1 * (x1 - x0) / (f1 - f0);
f = x*exp(1)^(-x/2)-exp(-1)/2;
index = 0;
r1 = 0.203656862188284;
res = zeros(1,3);

while abs(f) > 10^(-10)
    index = index + 1;
    x0 = x1;
    x1 = x;
    f0 = x0*exp(1)^(-x0/2)-exp(-1)/2;
    f1 = x1*exp(1)^(-x1/2)-exp(-1)/2;
    x = x1 - f1 * (x1 - x0) / (f1 - f0);
    f = x*exp(1)^(-x/2)-exp(-1)/2;
    residual = x - r1;
    fprintf('%3d %15.12f %10.2e\n', index, x, residual);
    res(index,1) = index;
    res(index,2) = x;
    res(index,3) = residual;
end
end