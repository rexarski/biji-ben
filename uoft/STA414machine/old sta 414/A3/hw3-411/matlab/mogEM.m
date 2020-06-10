% function [p,mu,vary,logProbtr] = mogEM(x,K,iters,minVary,plotFlag)
%
% Performs EM for a mixture of K axis-aligned (diagonal covariance
% matrix) Gaussians. iters iterations are used and the input variances are
% not allowed to fall below minVary (if minVary is not given, the default
% value is 0). The parameters are randomly initialized using the mean
% and variance of each input.
%
% Input:
%
%   x(:,t) = the N-dimensional training vector for the tth training case
%   K = number of Gaussians to use
%   iters = number of iterations of EM to apply
%   minVary = minimum variance of sensor noise (default: 0)
%   plotFlag = if flag=1 will plot color-coded 2-d data and clusters
%
% Output:
%
%   p = probabilities of clusters
%   mu(:,c) = mean of the cth cluster
%   vary(:,c) = variances for the cth cluster
%   logProbX(i) = log-probability of data after i-1 iterations
%

function [p,mu,vary,logProbX] = mogEM(x,K,iters,minVary,plotFlag)

if nargin==3 minVary = 0; plotFlag = 0; end;
N = size(x,1); T = size(x,2);

plotString = cellstr(['bo'; 'gx'; 'r+'; 'c*'; 'ms'; 'yd'; 'kd']);
ellColor = ['b'; 'g'; 'r'; 'c'; 'm'; 'y'; 'k'];

% Initialize the parameters
randConst = 1;
p = randConst+rand(K,1); p = p/sum(p);
mn = mean(x,2); vr = std(x,[],2).^2;

%-------------------- Modify the code here --------------------------------
% Change the random initialization with k-means algorithm, use 5
% iterations.
mu = mn*ones(1,K)+randn(N,K).*(sqrt(vr)/randConst*ones(1,K));

%------------------------------------------------------------------------
vary = vr*ones(1,K)*2; vary = (vary>=minVary).*vary + (vary<minVary)*minVary;

% Do iters iterations of EM
logProbX = zeros(iters,1);

for i=1:iters
  % Do the E step
  respTot = zeros(K,1); respX = zeros(N,K); 
  respDist = zeros(N,K); logProb = zeros(1,T);
  ivary = 1./vary;
  logNorm = log(p)-0.5*N*log(2*pi)-0.5*sum(log(vary'),2);
  logPcAndx = zeros(K,T);
  for k=1:K
    logPcAndx(k,:) = logNorm(k)...
                - 0.5*sum((ivary(:,k)*ones(1,T)).*(x-mu(:,k)*ones(1,T)).^2,1);
  end;
  [mx mxi] = max(logPcAndx,[],1); 
  PcAndx = exp(logPcAndx-ones(K,1)*mx); Px = sum(PcAndx,1);
  PcGivenx = PcAndx./(ones(K,1)*Px); logProb = log(Px) + mx;
  logProbX(i) = sum(logProb);

  % Plot log prob of data
  figure(1);
  set(gcf,'DoubleBuffer','on')
  clf;
  plot([0:i-1],logProbX(1:i),'r-');
  title('Log-probability of data versus # iterations of EM');
  xlabel('Iterations of EM');
  ylabel('log P(D)');
  drawnow;

  if plotFlag     % Plot the data and Gaussians
    figure(2);
    set(gcf,'DoubleBuffer','on')
    clf;
    hold on;
    for k=1:K
      plotEllipse(mu(1,k),mu(2,k),vary(1,k),vary(2,k),0,ellColor(mod(k, length(ellColor))+1));
    end;
    for t=1:T  plot(x(1,t),x(2,t),char(plotString(mod(mxi(t), length(plotString))+1))); end

    axis equal;
  end;

  respTot = mean(PcGivenx,2);
  respX = zeros(N,K); respDist = zeros(N,K);
  for k=1:K
    respX(:,k) = mean(x.*(ones(N,1)*PcGivenx(k,:)),2);
    respDist(:,k) = mean((x-mu(:,k)*ones(1,T)).^2.*(ones(N,1)*PcGivenx(k,:)),2);
  end;

  % Do the M step
  p = respTot;
  mu = respX./(ones(N,1)*respTot'+eps);
  vary = respDist./(ones(N,1)*respTot'+eps);
  vary = (vary>=minVary).*vary + (vary<minVary)*minVary;

end;
