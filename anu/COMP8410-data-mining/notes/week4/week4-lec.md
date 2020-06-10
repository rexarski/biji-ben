##  



describe which kind of data frequent pattern mining, assocaition mining?

very many heterogenous but simple items (nominal data) may be grouped into large (unordered) sets called transactions



for an assocaition rule A==>B what is A?

A is an itemset, i.e. a set of items. 



The XXXXX of itemset A in dataset D is the proportion number of transactions in D in which A is a subset / number of transactions in D
Here, XXXXX means

A. support count

B. confidence

C. relative support

D. suppot(A)

E. frequency



Consider association rules A ===> B and B ===> A(1) Is the support same or different for these two rules?(2) Is the confidence the same or different for these two rules?(3) Is the lift the same or different for these two rules?(4) Is Pearson's chi-square test the same or different for the two rules?

1. support does not distinguish between the sides of the arrow, it measures freq of association of A with B.
2. confid measures how often both itemsets occur together vs A occuring alone, so it does differentiate between A and B.
3. lift measures how much the prob of 
4. ...



Support and lift are **null-invariant**.

**False**



Closed frequent itemsets and/or maximal frequent itemsets save memory in frequent itemset mining because

**A**. **From the closed frequent itemsets with their counts, all the other frequent itemsets and their counts can be derived.**

B. From the maximal frequent itemsets with their counts, all the other frequent itemsets and their counts can be derived.

**C**. **From the maximal frequent itemsets with their counts, all the other frequent itemsets, but not their counts, can be derived.**

D. No clue, please help.



Let's say you have used the a-priori algorithm to generate frequent itemsets. How do you go about computing the strong association rules? 

Firstly, choose a frequent itemset, say  I = {A,B,C}. What are all the non-empty proper subsets?

{a},{b},{c},{a,b},{a,c},{b,c}



Then check whether the rule has confidence exceeding min_conf, and if so write it out.  Why do we not need to check support?





Closed frequent itemsets and/or maximal frequent itemsets save memory in frequent itemset mining because

**A. From the closed frequent itemsets with their support counts, all the other frequent itemsets and their support counts can be derived.**

B. From the maximal frequent itemsets with their support counts, all the other frequent itemsets and their  support counts can be derived.

**C. From the maximal frequent itemsets with their support counts, all the other frequent itemsets, but not their support counts, can be derived.**

D. No clue, please help.