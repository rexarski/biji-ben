function swinger(x0,y0)
% SWINGER  Classic double pendulum.
%   SWINGER(x,y) starts the pendulum at the given initial position.
%   The initial position can reset with the mouse.
%
%   SWINGER with no arguments starts at (x,y) = (0.862,-0.994).
%   What is interesting about the resulting orbit?
%
%   SWINGER(0,2) starts in an unstable vertical position.
%   How long does it stay there and what causes it to move?
%
%   The model is a pair of coupled second order nonlinear odes for
%   two angles.  The model is rewriten as first order system involving 
%      u = [theta1, theta2, theta1dot, theta2dot]'
%   The resulting equations are in implicit form, M*udot = f.

%   Copyright 2014 Cleve Moler
%   Copyright 2014 The MathWorks, Inc.

   
   % ------------------------
   
   function M = swingmass(t,u)
   
      % Mass matrix for classic double pendulum.
      c = cos(u(1)-u(2));
      M = [1 0 0 0; 0 1 0 0; 0 0 2 c; 0 0 c 1];
   end
      
   % ------------------------
      
   function f = swingrhs(t,u)
      % Driving force for classic double pendulum.
      g = 1;
      s = sin(u(1)-u(2));
      f = [u(3); u(4); -2*g*sin(u(1))-s*u(4)^2; -g*sin(u(2))+s*u(3)^2];
   end
      
   % ------------------------
      
   function theta = swinginit(x,y)
      % Angles to starting point.
      %   swinginit(0,-2) = [0 0]'
      %   swinginit(sqrt(2),0) = [3*pi/4 pi/4]'
      %   swinginit(0,2) = [pi pi]'
      
      r = norm([x,y]);
      if r > 2
         alpha = 0;
      else
         alpha = acos(r/2);
      end
      beta = atan2(y,x) + pi/2;
      theta = [beta+alpha; beta-alpha];
   end
      
   % ------------------------
      
   function status = swingplot(t,u,task)
      % Plot function for classic double pendulum.

      persistent plt titl orbt erasemode
      
      if ~isequal(task,'done')
      
         % Coordinates of both bobs
         
         theta = u(1:2);
         x = cumsum(sin(theta));
         y = cumsum(-cos(theta));
         
         switch task
         
            case 'init'
         
               % Initialize plot
         
               orbt  = findobj('string','orbit');
               erasemode = verLessThan('matlab','8.4');

               if get(orbt,'value')
                  if erasemode
                     plt = plot([x(2) x(2)],[y(2) y(2)],'-','erasemode','none');
                  else
                     set(plt,'vis','off')
                     drawnow
                     plt = animatedline([x(2) x(2)],[y(2) y(2)]);
                  end
               else
                  plt = plot([0; x],[0; y],'o-');
               end
               axis(2.25*[-1 1 -1 1])
               axis square
               xlabel('Click to reinitialize');
               if erasemode
                  titl = title(sprintf('t = %8.1f',t),'erasemode','xor');
               else
                  titl = title(sprintf('t = %8.1f',t));
               end
         
            case ''
         
               % Update plot
         
               if get(orbt,'value')
                  if erasemode
                     xo = get(plt,'xdata');
                     yo = get(plt,'ydata');
                     set(plt,'xdata',[xo(2) x(2)],'ydata',[yo(2) y(2)])
                  else
                     addpoints(plt,x(2),y(2))
                  end
               else
                  set(plt,'xdata',[0; x],'ydata',[0; y])
               end
         
               % Display time in title
         
               set(titl,'string',sprintf('t = %8.1f',t));
               drawnow
         end
      
         % Terminate ode solver after mouse click
      
         status = ~isempty(get(gca,'userdata'));
      end
   end

   % ------------------------
   
   % Default initial position
   
   if nargin < 2
      x0 = 0.862;
      y0 = -0.994;
   end

   % Initialize figure and buttons.
   % Click on figure to save the point in current axis userdata.
   
   clf reset
   shg
   set(gcf,'name','Swinger','menu','none','numbertitle','off', ...
      'windowbuttonup','set(gca,''userdata'',get(gca,''currentpoint''))')
   orbit = uicontrol('style','toggle','string','orbit','value',0, ...
      'units','normalized','position',[.02 .02 .09 .05], ...
      'callback','set(gca,''userdata'',''orbit'')');
   stop = uicontrol('style','toggle','string','stop','value',0, ...
      'units','normalized','position',[.90 .02 .09 .05], ...
      'callback','set(gca,''userdata'',''stop'')');
   
   % Restart ode solver after each mouse click
   
   while get(stop,'value') == 0
      axisdata = get(gca,'userdata');
      if isempty(axisdata)
         theta0 = swinginit(x0,y0);
      elseif ischar(axisdata)
         theta0 = get(gcf,'userdata');
      else
         x0 = axisdata(1,1);
         y0 = axisdata(1,2);
         % If close to vertical, make it exactly vertical
         if abs(x0) < .01 & y0 > 2
            x0 = 0; y0 = 2;
         end
         theta0 = swinginit(x0,y0);
      end
      set(gcf,'userdata',theta0)
      set(gca,'userdata',[])
   
      % Start the ode solver
   
      u0 = [theta0; 0; 0];
      tspan = [0 1.e6];
      opts = odeset('mass',@swingmass,'outputfcn',@swingplot,'maxstep',0.02);
      ode23(@swingrhs,tspan,u0,opts);
   end
   delete(orbit);
   set(stop,'style','push','string','close','callback','close(gcf)');

end
