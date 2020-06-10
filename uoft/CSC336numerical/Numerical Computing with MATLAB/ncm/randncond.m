% RANDNCOND  Condition of random matrices

%   Copyright 2014 Cleve Moler
%   Copyright 2014 The MathWorks, Inc.

nmax = 100;
n = 2:nmax;
kappalo = n.^(1/2);
kappahi = 500*n.^3;

shg
clf reset
h = loglog(n,[kappalo; kappahi],'-',nmax,NaN,'.');
set(h(1:2),'color',[0 2/3 0]);
set(h(3),'color','blue')
set(gca,'xtick',[2:2:10 20:20:nmax])
kappamax = 1.e6;
axis([2 nmax 2 kappamax])
stop = uicontrol('pos',[20 10 40 25], ...
   'style','toggle','string','stop','value',0);
hold on

while get(stop,'value') ~= 1
   n = ceil(rand*nmax);
   A = randn(n,n);
   kappa = condest(A);
   loglog(n,kappa,'.','color','blue')
   drawnow
end
hold off

set(stop,'val',0,'string','close','callback','close(gcf)')
