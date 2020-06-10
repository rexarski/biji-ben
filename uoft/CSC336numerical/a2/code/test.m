% Take g = 10, v = 6 as constants.
n = 4;
m = linspace(50, 100, n);
c = 25 - 10*linspace(0, 1, n);
b = transpose(6.*c -10.*m);
e = ones(n, 1);
A = spdiags([-e, e], [-1, 0], n, n);
A(:, n) = -m;
tension = A\b;
display(tension); % output of tension vector
max_tension = max(tension);
display(max_tension); % output of maximum tension computed

for i = 2:4
    ha = ((c(i-1)+c(i))-sum(c)/sum(m)*(m(i-1)+m(i)))*6;
    display(ha)
end