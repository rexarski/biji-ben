# Question 3: A* Search
## _An Informed Search Algorithm_ (20 Marks)

### What We Expect You To Do

Implement the A* search algorithm inside the `solve()` function in
[`a_star_search.py`](../a_star_search.py).

Your A* search will use the heuristic contained in the `heuristic` argument
passed to the `solve()` function in [`a_star_search.py`](../a_star_search.py).
The heuristics take a state and return an estimate of the cost to reach the
goal from that state. The heuristics are defined in
[heuristics.py](../heuristics.py) and for the simple navigation search problem
we include three heuristics:

- The null heuristic, i.e. `h(s) = 0` for every state `s`,
- the Manhattan distance heuristic, `h(s) = |x(s) - x(G)| + |y(s) - y(G)|`,
  where `x()` and `y()` are the coordinates of the given state `s` or goal
  state `G`,
- and the Euclidean distance heuristic,
  `h(s) = sqrt( |x(s) - x(G)|^2 + |y(s) - y(G)|^2 )`.

Your implementation of A* needs to have **all** of the following properties:

1. It implemments graph search rather than tree search.
2. It returns a **valid** sequence of actions. That is, all moves are legal and
   the sequence of moves leads from the initial state to the goal.
3. The sequence of actions has the **optimal length** when using an admissible
   heuristic (such as the *Manhattan Distance* and the *Euclidean Distance*
   heuristic)
4. It visits states in the **right** order. That is, it expands nodes with
   smaller f-values first.
5. Your implementation is not substantially slower than our solution over the
   maps `anuSearch`, `aiSearch` and `mazeSearch`.
6. When given an admissible heuristic (which is not necessarily consistent),
   your A* search must return an optimal solution.

The times and costs of optimal solutions with our implementation on the three
maps mentioned above are:

| Problem    | Cost | Expanded Manhattan | Time w. Manhattan (secs) | Expanded Euclidean | Time w. Euclidean (secs) |
| ---------- | ---- | ------------------ | ------------------------ | ------------------ | ------------------------ |
| anuSearch  | 45   | 222                | 0.0084                   | 200                | 0.0076                   |
| aiSearch   | 26   | 59                 | 0.0024                   | 89                 | 0.00425                  |
| mazeSearch | 68   | 222                | 0.005                    | 226                | 0.005                    |


The times above have been averaged over several runs. The measurements were
taken using Anaconda Python 3.6.3 on a 2014 MacBook Pro (2.8 GHz Intel Core
i7). Depending on the implementation, your number of expanded nodes might
differ from the above.

You can test your implementation with the commands:

```
python3 red_bird.py -l search_layouts/anuSearch.lay -p SearchAgent -a fn=astar,heuristic=manhattan
python3 red_bird.py -l search_layouts/aiSearch.lay -p SearchAgent -a fn=astar,heuristic=manhattan
python3 red_bird.py -l search_layouts/mazeSearch.lay -p SearchAgent -a fn=astar,heuristic=manhattan
```

Alternatively, if you're using Mac or Linux, you can run these shortcuts:

```sh
./testAStar.sh anuSearch manhattan
./testAStar.sh aiSearch manhattan
./testAStar.sh mazeSearch manhattan
```

Replace `manhattan` with `euclidean` to change the heuristic.

### Hints

1. A* **expands** first the nodes on the frontier with *minimum f-value*.
2. In [frontiers.py](../frontiers.py) you will find a number of data structures
   readily available for you to use.
3. Be sure to avoid generating a path to the same state more than once.
4. When you need to find the heuristic value of a state, the usage of the heuristic will typically be of the form `heuristic_value = heuristic(state, problem)`.

### What to Submit

You need to include in your submission the file `a_star_search.py` with your
implementation of A*. Please, remember to fill in your details in the comments
at the start of the file.

Once you've finished, you can move to the [next section](6_heuristics.md) or go
back to the [index](README.md).
