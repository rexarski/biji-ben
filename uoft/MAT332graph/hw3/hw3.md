# chapter 2

Q1. Let M be a matching in a bipartite graph G. Show that if M is suboptimal, i.e. contains fewer edges than some other matching in G, then G contains an augmenting path with respect to M. Does this fact generalize to matchings in non-bipartite graphs?

Hint: Recall how an augmenting path turns a given matching into a larger one. Can you reverse this process to obtain an augmenting path from the two matchings?

[page 1 question 3](http://homepage.cs.uiowa.edu/~sriram/137/spring05/hw1Solution.pdf)

Q5. Derive the marriage theorem from K¨onig’s theorem.

Hint: If there is no matching of A, then by K¨onig’s theorem few vertices cover all the edges. How can this assumption help you to ﬁnd a large subset of A with few neighbours?

[problem 2](http://www.sfu.ca/~mdevos/345/homework6_sol.pdf)

Q7. Find an inﬁnite counterexample to the statement of the marriage theorem.

Hint: If you have S proper subset in S' ⊆ A with |S| = |N(S)| in the ﬁnite case, the marriage condition ensures that N(S) proper subset N(S'): increasing S makes more neighbours available. Use the fact that this fails when S is inﬁnite.

[the first problem is a solution](http://homepages.math.uic.edu/~mubayi/591GT/hw2sol.pdf) or [q5 here](http://www.cs.bilkent.edu.tr/~ugur/teaching/cs570/assignment/hw2sol.pdf)

Q8. Let k be an integer. Show that any two partitions of a ﬁnite set into k-sets admit a common choice of representatives.

Hint: Apply the marriage theorem.

[5)](http://homepages.math.uic.edu/~mubayi/591GT/hw2sol.pdf)
[better](http://www.austinmohr.com/Work_files/mohr%20hw2.pdf)

Q11. Let G be a bipartite graph with bipartition {A, B}. Assume that δ(G) >= 1, and that d(a) >= d(b) for every edge ab with a ∈ A. Show that G contains a matching of A.

Hint: Intuitively, the edges between a set S ⊆ A and N(S) create larger degrees in S than in N(S), so they must be spread over more vertices of N(S) than of S. To make this precise, count both S and N(S) as a sum indexed by those edges. Alternatively, consider a minimal set S violating the marriage condition, and count the edges between S and N(S) in two ways.

[page 1, first problem](http://people.math.sc.edu/lu/teaching/2013fall_776/homework4_sol.pdf)

Q12. Find a bipartite graph with a set of preferences such that no matching of maximum size is stable and no stable matching has maximum size. Find a non-bipartite graph with a set of preferences that has no stable matching.

Hint: For the second task, remember that change occurs most likely if unhappy vertices can bring it about without having to ask the happy ones. If philosophy does not help, try K^3.

[DO IT YOURSELF]

Q13. Consider the algorithm described in the proof of the stable marriage theorem. Observe that once a vertex of B is matched, she remains matched and gets happier with every change of her matching edge. On the other hand, show that the sequence of matching edges incident with a given vertex of A makes this vertex unhappier with every change (disregarding the interim periods when he is unmatched).

Hint: Consider the transition from a matching edge ab to a later matching edge ab' . Suppose a prefers b' to b. Why did he not marry b' in the ﬁrst place?

[page2, first theorem proof?](http://www.cs.hunter.cuny.edu/~saad/courses/493.55/notes/note7.pdf)

Q14. Show that all stable matchings of a given graph cover the same vertices. (In particular, they have the same size.)

Hint: Alternating paths.

[page 1, second problem](http://people.math.sc.edu/lu/teaching/2013fall_776/homework4_sol.pdf)

Q19. Find a cubic graph without a 1-factor.

Hint: Corollary 2.2.2.

[Page 17, upper half](http://web.thu.edu.tw/wang/www/1factor_Cubic/FactorBook(Chapter1).pdf)


# chapter 3

Q1. let G be a graph with vertices a and b, and let X ⊆ V (G) \ {a, b} be an a–b separator in G. Show that X is minimal as an a–b separator if and only if every vertex in X has a neighbour in the component C\_a of G − X containing a, and another in the component C\_b of G − X containing b.

Hint: Recall the deﬁnitions of ‘separate’ and ‘component’.

Q7. Show that the block graph of any connected graph is a tree.

Hint: Deduce the connectedness of the block graph from that of the graph itself, and its acyclicity from the maximality of each block.

Q8. Let G be a k-connected graph, and let xy be an edge of G. Show that G/xy is k-connected if and only if G − {x, y} is (k − 1)-connected.

Hint: Assuming that G/xy is not k-connected, distinguish the cases when v_{xy} lies inside or outside a separator of at most k − 1 vertices.

Q10. Let e be an edge in a 3-connected graph G != K^4 . Show that either G − e (there is a dot on the -) or . G/e is again 3-connected.

Hint: Suppose that both after contracting e and after deleting e there is a 2-separator in the resulting graph. How are these separators arranged with respect to each other?

[page 5, problem 6](http://people.math.sc.edu/lu/teaching/2013fall_776/homework4_sol.pdf)

Q15. Find the error in the following ‘simple proof’ of Menger’s theorem (3.3.1). Let X be an A–B separator of minimum size. Denote by G\_A the subgraph of G induced by X and all the components of G − X that meet A, and deﬁne G\_B correspondingly. By the minimality of X, there can be no A–X separator in G\_A with fewer than |X| vertices, so G\_A contains k disjoint A–X paths by induction. Similarly, G\_B contains k disjoint X–B paths. Together, all these paths form the desired A–B paths in G.

Hint: Check the induction.

Q16. Prove Menger’s theorem by induction on ||G||, as follows. Given an edge e = xy, consider a smallest A–B separator S in G − e. Show that the induction hypothesis implies a solution for G unless S ∪ {x} and S ∪ {y} are smallest A–B separators in G. Then show that if choosing neither of these separators as X in the previous exercise gives a valid proof, there is only one easy case left to do.

Hint: How big is S? To recognize the easy remaining case, it helps to have solved the previous exercise ﬁrst.

Q19. Let k >= 2. Show that in a k-connected graph any k vertices lie on a common cycle.

Hint: Consider a cycle through as many of the k given vertices as possible. If one them is missed, can you re-route the cycle through it?
