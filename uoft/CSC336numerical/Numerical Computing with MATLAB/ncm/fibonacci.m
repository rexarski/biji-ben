function f = fibonacci(n)
%FIBONACCI  Fibonacci sequence
%   f = FIBONACCI(n) generates the first n Fibonacci numbers.

%   Copyright 2014 Cleve Moler
%   Copyright 2014 The MathWorks, Inc.

f = zeros(n,1);
f(1) = 1;
f(2) = 2;
for k = 3:n
   f(k) = f(k-1) + f(k-2);
end
