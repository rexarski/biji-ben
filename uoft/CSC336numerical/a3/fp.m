function res = fp(x)
format long
g = exp(-1)/2*exp(1)^(x/2);
index = 0;
diff = abs(g-x);
res = zeros(1,3);

while diff > 10^(-10)
    index = index + 1;
    x = g;
    g = exp(-1)/2*exp(1)^(x/2);
    diff = abs(g-x);
    fprintf('%3d %15.12f %10.2e\n', index, x, diff);
    res(index,1) = index;
    res(index,2) = x;
    res(index,3) = diff;
end
end