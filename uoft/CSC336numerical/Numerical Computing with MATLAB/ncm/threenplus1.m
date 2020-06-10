function threenplus1R(n)
%"Three n plus 1".
%   Study the 3n+1 sequence.
%   threenplus1(n) plots the sequence starting with n.
%   threenplus1 with no arguments starts with n = 1.
%   uicontrols decrement or increment the starting n.
%   Is it possible for this to run forever?

%   Copyright 2014 Cleve Moler
%   Copyright 2014 The MathWorks, Inc.

if ~isequal(get(gcf,'tag'),'3n+1')
   shg
   clf reset
   set(gcf,'menu','none','numbertitle','off','name','3n+1')
   uicontrol( ... 
      'units','normalized',...
      'position',[0.455, 0.01, 0.044, 0.054], ...
      'string','<','fontunits','normalized','fontsize',0.6,...
      'callback','threenplus1(''<'')');
   uicontrol( ...
      'units','normalized',...
      'position',[0.525, 0.01, 0.044, 0.054],...
      'string','>','fontunits','normalized','fontsize',0.6, ...
      'callback','threenplus1(''>'')');
   uicontrol( ...
      'units','normalized',...
      'position',[0.842, 0.01, 0.07, 0.054], ...
      'string','close','fontunits','normalized','fontsize',0.6, ...
      'callback','close(gcf)')
   set(gcf,'tag','3n+1');
end

if nargin == 0
   n = 2;
elseif isequal(n,'<')
   n = get(gcf,'userdata') - 1;
elseif isequal(n,'>')
   n = get(gcf,'userdata') + 1;
end
if n < 1, n = 1; end
set(gcf,'userdata',n)

y = n;
while n > 1
   if rem(n,2)==0
      n = n/2;
   else
      n = 3*n+1;
   end
   y = [y n];
end

semilogy(y,'.-')
axis tight
ymax = max(y);
ytick = [2.^(0:ceil(log2(ymax))-1) ymax];
if length(ytick) > 8, ytick(end-1) = []; end
set(gca,'ytick',ytick)
Htitle=title(['n = ' num2str(y(1))]);
set(Htitle,'fontunits','normalized','fontsize',0.04)
