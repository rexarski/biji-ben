% Take g = 10, v = 6 as constants.
% (a) part i
kappa_vec = [];
t = zeros(32, 4);
ni = [4, 8, 16, 32];
for i = 1:4
    n = ni(i);
    m = linspace(50, 100, n);
    c = 25 - 10*linspace(0, 1, n);
    b = transpose(6.*c -10.*m);
    e = ones(n, 1);
    A = spdiags([-e, e], [-1, 0], n, n);
    A(:, n) = -m;
    tension = A\b;
    display(tension); % output of tension vector
    kappa = condest(A);
    display(kappa); % output of condition number of the matrix
    max_tension = max(tension);
    display(max_tension); % output of maximum tension computed
    kappa_vec = [kappa_vec, kappa]; % store condtion number
    t(1:n,i) = tension; % store tension vectors
end
figure
loglog([4 8 16 32], kappa_vec, 'k.-') % plot condition number vs. n
grid

figure
plot((1:ni(1)-1)/ni(1), t(1:ni(1)-1, 1), 'r-', ...
   (1:ni(2)-1)/ni(2), t(1:ni(2)-1, 2), 'g--', ...
   (1:ni(3)-1)/ni(3), t(1:ni(3)-1, 3), 'b-.', ...
   (1:ni(4)-1)/ni(4), t(1:ni(4)-1, 4), 'k.');
grid
