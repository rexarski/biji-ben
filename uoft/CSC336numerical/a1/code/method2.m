function [] = method2(yNK)
q=0.018350467697256206326;
digits(40);
for K = (3:1:9)
    for i = 1:K
        if i == 1
            previous = yNK;
        end
        y(21+K-i) = (previous + 1/exp(1))/(i+1);
        previous = y(21+K-i);
    end
    fprintf('%3d %20.16f %20.16f %10.6e\n', 20, y(21), q, q-y(21));
end
end