function fern
%FERN  MATLAB implementation of the Fractal Fern.
%   Michael Barnsley, Fractals Everywhere, Academic Press, 1993.
%   This version runs forever, or until stop is toggled.
%   See also FINITEFERN.

%   Copyright 2014 Cleve Moler
%   Copyright 2014 The MathWorks, Inc.

shg
clf reset
set(gcf,'color','white','menubar','none', ...
   'numbertitle','off','name','Fractal Fern')
x = [.5; .5];
darkgreen = [0 2/3 0];
plot(x(1),x(2),'.','markersize',4,'color',darkgreen)
axis([-3 3 0 10])
axis off
stop = uicontrol('style','toggle','string','stop', ...
   'background','white');
drawnow
hold on

p  = [ .85  .92  .99  1.00];
A1 = [ .85  .04; -.04  .85];  b1 = [0; 1.6];
A2 = [ .20 -.26;  .23  .22];  b2 = [0; 1.6];
A3 = [-.15  .28;  .26  .24];  b3 = [0; .44];
A4 = [  0    0 ;   0   .16];

cnt = 1;
tic
while ~get(stop,'value')
   r = rand;
   if r < p(1)
      x = A1*x + b1;
   elseif r < p(2)
      x = A2*x + b2;
   elseif r < p(3)
      x = A3*x + b3;
   else
      x = A4*x;
   end
   plot(x(1),x(2),'.','markersize',4,'color',darkgreen)
   drawnow
   cnt = cnt + 1;
end
t = toc;
s = sprintf('%8.0f points in %6.3f seconds',cnt,t);
text(-1.5,-0.5,s,'fontweight','bold');
set(stop,'style','pushbutton','string','close','callback','close(gcf)')
hold off
