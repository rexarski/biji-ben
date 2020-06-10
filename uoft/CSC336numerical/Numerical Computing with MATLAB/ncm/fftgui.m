function fftgui(y)
%FFTGUI  Demonstration of Finite Fourier Transform.
%  FFTGUI(y) plots real(y), imag(y), real(fft(y)) and imag(fft(y)).
%  FFTGUI, without any arguments, uses y = zeros(1,32).
%  When any point is moved with the mouse, the other plots respond.
%
%  Inspired by Java applet by Dave Hale, Stanford Exploration Project,
%     http://sepwww.stanford.edu/oldsep/hale/FftLab.html

%   Copyright 2014 Cleve Moler
%   Copyright 2014 The MathWorks, Inc.

if nargin == 0
   % Default initial y is all zeros.
   y = zeros(1,32);
end
if ~isempty(y)
   if isequal(y,'reset')
      % Restore original data
      y = get(0,'userdata');
      set(gcf,'userdata',y);
      set(findobj('tag','fftguirc'),'string','close', ...
         'callback','close(gcf)')
   else
      % Save input data.
      y = y(:)';
      set(0,'userdata',y);

      % Initialize figure.
      clf reset
      set(gcf, ...
        'name','Fftgui', ...
        'menu','none', ...
        'numbertitle','off', ...
        'units','normalized', ...
        'pos',[.05 .25 .90 .65], ...
        'windowbuttondownfcn', ...
        'fftgui([]); set(gcf,''windowbuttonmotionfcn'',''fftgui([])'')', ...
        'windowbuttonupfcn', ...
        'set(gcf,''windowbuttonmotionfcn'','''')')
      uicontrol('tag','fftguirc','string','close','callback','close(gcf)');
   end
   
   % Handles for plots

   n = length(y);
   lines = zeros(n,4);
   dots = zeros(1,4);  

   % Initialize four subplots

   x = 1:n;
   z = fft(y);
   
   subplot(221)
   plot([0 n+1],[0 0],'k-')
   axis([0 n+1 -1 1])
   u = real(y);
   lines(:,1) = line([x;x],[0*u;u],'color','cyan');
   dots(1) = line(x,u,'marker','.','markersize',16,'color','blue');
   set(gca,'xtick',[])
   set(gca,'ytick',[])
   title('real(y)','fontname','courier','fontweight','bold')
   
   subplot(222)
   plot([0 n+1],[0 0],'k-')
   axis([0 n+1 -1 1])
   u = imag(y);
   lines(:,2) = line([x;x],[0*u;u],'color','cyan');
   dots(2) = line(x,u,'marker','.','markersize',16,'color','blue');
   set(gca,'xtick',[])
   set(gca,'ytick',[])
   title('imag(y)','fontname','courier','fontweight','bold')
   
   subplot(223)
   plot([0 n+1],[0 0],'k-')
   axis([0 n+1 -2 2])
   u = real(z);
   lines(:,3) = line([x;x],[0*u;u],'color','cyan');
   dots(3) = line(x,u,'marker','.','markersize',16,'color','blue');
   set(gca,'xtick',[])
   set(gca,'ytick',[])
   title('real(fft(y))','fontname','courier','fontweight','bold')
   
   subplot(224)
   plot([0 n+1],[0 0],'k-')
   axis([0 n+1 -2 2])
   u = imag(z);
   lines(:,4) = line([x;x],[0*u;u],'color','cyan');
   dots(4) = line(x,u,'marker','.','markersize',16,'color','blue');
   set(gca,'xtick',[])
   set(gca,'ytick',[])
   title('imag(fft(y))','fontname','courier','fontweight','bold')

   % Save y and handles in figure userdata

   set(gcf,'userdata',{y,lines,dots})
  
else

   % Respond to mouse motion.
   fud = get(gcf,'userdata');
   y = fud{1};
   n = length(y);
   pt = get(gcf,'currentpoint');
   pos = get(gca,'pos');
   p = round((n+1)*(pt(1)-pos(1))/pos(3));
   q = 2*(pt(2)-pos(2))/pos(4)-1;
   kase = 1 + (pt(1)>.5) + 2*(pt(2)<.5);
   if (p > 0) & (p < n+1) & (abs(q) <= 1)
      switch kase
         case 1 
            y(p) = q+i*imag(y(p));
            z = fft(y);
         case 2 
            y(p) = real(y(p))+i*q;
            z = fft(y);
         case 3
            z = fft(y);
            z(p) = 2*q+i*imag(z(p));
            y = ifft(z);
         case 4 
            z = fft(y);
            z(p) = real(z(p))+i*2*q;
            y = ifft(z);
      end
      
      lines = fud{2};
      dots = fud{3};
      set(dots(1,1),'ydata',real(y))
      set(dots(1,2),'ydata',imag(y))
      set(dots(1,3),'ydata',real(z))
      set(dots(1,4),'ydata',imag(z))
      for k = 1:n
         set(lines(k,1),'ydata',[0 real(y(k))])
         set(lines(k,2),'ydata',[0 imag(y(k))])
         set(lines(k,3),'ydata',[0 real(z(k))])
         set(lines(k,4),'ydata',[0 imag(z(k))])
      end
      set(gcf,'userdata',{y,lines,dots});
      set(findobj('tag','fftguirc'),'string','reset', ...
         'callback','fftgui(''reset'')')
   end
end
