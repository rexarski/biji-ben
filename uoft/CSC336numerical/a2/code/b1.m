% (b)
ni = 8;
m = linspace(50, 100, ni);
c = 25 - 10*linspace(0, 1, ni);
b = 6.*c -10.*m;
e = ones(ni, 1);
A = spdiags([-e, e], [-1, 0], ni, ni);
A(:, ni) = -m;
[L, U, P] = lu(A);
display(L);
display(U);
display(P);