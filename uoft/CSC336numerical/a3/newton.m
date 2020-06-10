function res = newton(x)
format long
f = x*exp(1)^(-x/2)-exp(-1)/2;
fprime = (1-x/2)*exp(1)^(-x/2);
index = 0;
r1 = 0.203656862188284;
res = zeros(1,3);

while abs(f) > 10^(-10)
    index = index + 1;
    x = x-f/fprime;
    f = x*exp(1)^(-x/2)-exp(-1)/2;
    fprime = (1-x/2)*exp(1)^(-x/2);
    residual = x - r1;
    fprintf('%3d %15.12f %10.2e\n', index, x, residual);
    res(index,1) = index;
    res(index,2) = x;
    res(index,3) = residual;
end
end