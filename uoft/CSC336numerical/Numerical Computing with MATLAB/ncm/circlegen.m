function circlegen(h)
%CIRCLEGEN  Generate approximate circles.
%   CIRCLEGEN(h) uses step size h.
%   CIRCLE with no arguments uses h = 0.20906.

%   Copyright 2014 Cleve Moler
%   Copyright 2014 The MathWorks, Inc.

if nargin < 1
   h = sqrt(2*(1-cos(2*pi/30)));
end

shg
clf
set(gcf,'menu','none','numbertitle','off','name','Circlegen')
z = exp(2*pi*i*(0:256)/256);
grey = [.8 .8 .8];
p = plot(real(z),imag(z),'-',0,0,'o',1,0,'.');
set(p(1:2),'color',grey);
p = p(3);
set(p,'color','black');
if verLessThan('matlab','8.4')
   set(p,'erasemode','none')
end
axis([-2 2 -2 2])
axis square
title(['h = ' num2str(h)])
stop = uicontrol('style','toggle','string','stop');

x = 1;
y = 0;
while ~get(stop,'value')
   x = x + h*y;
   y = y - h*x;
   set(p,'xdata',x,'ydata',y);
   drawnow
end

set(stop,'string','close','value',0,'callback','close')
