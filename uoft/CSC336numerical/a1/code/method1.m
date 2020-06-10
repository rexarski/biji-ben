function [] = method1(y0)
N = 20;
for i = 1:(N)
    if i == 1
        previous = y0;
    end
    y(i) = -1/exp(1) + i * previous;
    fprintf('%3d %20.16f\n', i-1, y(i));
    previous = y(i);
end
end
