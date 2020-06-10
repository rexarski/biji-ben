disp('fixed-point:');
res1 = fp(0);
disp('Newton:');
res2 = newton(0);
disp('secant:');
res3 = secant(0,2);
r1 = 0.203656862188284;

figure
semilogy(res1(:,1),abs(res1(:,2)-r1),'--');
hold on
semilogy(res2(:,1),abs(res2(:,3)),'-.');
hold on
semilogy(res3(:,1),abs(res3(:,3)),'-');
grid;