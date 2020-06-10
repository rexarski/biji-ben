function [] = plotEllipse(mu1,mu2,var1,var2,covar,colorChar)
 
t = -pi:.01:pi;
k = length(t);
x = 1*sin(t);
y = 1*cos(t);

R = [var1 covar; covar var2];

[vv, dd] = eig(R);

A = real((vv * sqrt(dd))');
z = [x' y'] * A;

hold on;
plot(z(:,1)+mu1,z(:,2)+mu2,colorChar);
plot(mu1,mu2,strcat(colorChar,'h'));
