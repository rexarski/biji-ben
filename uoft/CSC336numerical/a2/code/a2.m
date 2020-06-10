% (a) part ii


t = zeros(32, 4);
ni = [4, 8, 16, 32];
for i = 1:4
    n = ni(i);
    m = sort(50 + 50*rand(n, 1), 'ascend');
    c = sort(15 + 10*rand(n, 1), 'descend');
    b = 6.*c -10.*m;
    e = ones(n, 1);
    A = spdiags([-e, e], [-1, 0], n, n);
    A(:, n) = -m;
    tension = A\b;
    display(tension); % output of tension vector
    max_tension = max(tension);
    display(max_tension); % output of maximum tension computed
    t(1:n,i) = tension; % store tension vectors
end

plot((1:ni(1)-1)/ni(1), t(1:ni(1)-1, 1), 'r-', ...
   (1:ni(2)-1)/ni(2), t(1:ni(2)-1, 2), 'g--', ...
   (1:ni(3)-1)/ni(3), t(1:ni(3)-1, 3), 'b-.', ...
   (1:ni(4)-1)/ni(4), t(1:ni(4)-1, 4), 'k.');
