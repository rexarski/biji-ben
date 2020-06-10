% function [dist] = distmat(v1, v2)
% 
% Calculates pairwise distances between vectors. If v1 and v2 are both
% provided, a size(v1, 1) by size(v2, 1) matrix is returned, where the
% entry at (i,j) contains the Euclidean distance from v1(i,:) to v2(j,:).
% If only v1 is provided, squareform(pdist(v1)) is returned.

function [dist] = distmat(p, q, disttype)
	p = p';
	if nargin == 1
		q = p;
	else
		q = q';
	end

	[d, pn] = size(p);
	[d, qn] = size(q);

	pmag = sum(p .* p, 1);
	qmag = sum(q .* q, 1);
	dist = repmat(qmag, pn, 1) + repmat(pmag', 1, qn) - 2*p'*q;
	dist = sqrt(dist);
