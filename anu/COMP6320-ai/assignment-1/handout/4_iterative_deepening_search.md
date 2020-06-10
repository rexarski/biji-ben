# Question 2: Iterative Deepening Search
## _Another uninformed but less memory consuming algorithm_ (15 Marks)

### What We Expect You To Do

Implement the Iterative Deepening Search (IDS) algorithm inside the `solve()`
function in [`ids_search.py`](../ids_search.py).

Remember from the lectures that this search algorithm performs a series of
depth-limited Depth First Searches (DFS). This enables it to combine the
completeness and optimality guarantees of BrFS, with low space requirements of
DFS `O(bm)`, at the extra cost of exploring the same prefix of the search tree
many times. Remember also that DFS expands always the deepest node on the
frontier first, and this can be implemented using a LIFO (Last In First Out)
policy.

Your implementation of IDS needs to have **all** of the following properties:

1. It returns a **valid** sequence of actions. That is, all moves are legal and
   the sequence of moves leads from the initial state to the goal.
2. It visits states in the **right** order. See description of IDS in the
   lectures for more info.
3. It produces an **optimal** solution. That is, the number of steps is
   minimal.
4. As the depth of the deepest node increases, the number of nodes on the
   frontier grows **linear** with it. That is, the space complexity needs to
   be `O(bd)`, where `b` is the branching factor and `d` is the depth.
5. In case no solution is found, the procedure prints on the standard
   output/console a **lower-bound** of the optimal cost. That is, if we need to
   manually terminate your program early (with Ctrl-C), we should still be able
   to find out what the lower bound of the cost should be.
6. Your implementation is not substantially slower than our solution over the
   maps `anuSearch`, `aiSearch` and `mazeSearch`.

To get an idea of how fast your implementation should run, here are the times
of our solution on the three maps, `anuSearch`, `aiSearch` and `mazeSearch`:

| Problem    | Cost | Expanded   | Time (secs) |
|------------|------|------------|-------------|
| anuSearch  | 45   | timeout    | timeout     |
| aiSearch   | 26   | 43,652,859 | 400         |
| mazeSearch | 68   | 16,469     | 0.15        |

Note that our baseline solution was not able to produce a result for the
`anuSearch` map within 30 minutes. The measurements were taken using Anaconda
Python 3.6.3 on a 2014 MacBook Pro (2.8 GHz Intel Core i7). Depending on the
implementation, your number of expanded nodes might differ from the above.

Even if you manage to
solve all of the three maps above, you still need to fulfill requirement 5 on
printing out the lower bound, as we may test your solution on more difficult
maps.

You can test your implementation with the commands:

```
python3 red_bird.py -l search_layouts/anuSearch.lay -p SearchAgent -a fn=ids
python3 red_bird.py -l search_layouts/aiSearch.lay -p SearchAgent -a fn=ids
python3 red_bird.py -l search_layouts/mazeSearch.lay -p SearchAgent -a fn=ids
```

Alternatively, if you're using Mac or Linux, you can run these shortcuts:

```sh
./testIDS.sh anuSearch
./testIDS.sh aiSearch
./testIDS.sh mazeSearch
```

### Hints

1. At each iteration, IDS **expands** first the *deepest* nodes on the frontier.
2. In [frontiers.py](../frontiers.py) you will find a number of data
   structures readily available for you to use.
3. The depth-first implementation can be either the recursive or iterative (see
   lectures).
4. In order to at least achieve the above benchmark, you need a smart way to
   detect loops, which does not compromise optimality, and preserves the
   `O(bm)` space requirement.
5. In order to print the lower bound, note that IDS contains a main loop. Every
   time an iteration of this loop fails to produce a result, that gives you
   some information about the lower bound. You only need to print your lower
   bound estimate to the screen as soon as the estimate increases, regardless
   of whether or not you think the search may eventually be successful.
   You should end up with a monotonically increasing series of estimates
   printed to the terminal, regardless of whether the search times out or not.

### What to Submit

You need to include in your submission the file `ids_search.py` with your
implementation of IDS. Please, remember to fill in your details in the
comments at the start of the file.

Once you've finished, you can move to the [next section](5_a_star.md) or go
back to the [index](README.md).
