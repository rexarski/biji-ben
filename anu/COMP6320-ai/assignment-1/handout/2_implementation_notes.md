# Implementation details: The Fundamentals

This part of the handout explains some basic facts and concepts you need to be
familiar with in order to complete the tasks in the assignment. Skip it at your
own risk!

## The search infrastructure for the single-agent collecting birds problem

Your search algorithms needs to return a list of actions that reaches
the goal from the start state in the given problem. The elements of this list
need to be one or more references to the attributes `NORTH`, `SOUTH`, `EAST`
and `WEST` of the class [`Directions`](../actions.py).

Your search algorithms will be passed as an argument an instance of either the
class [SearchProblem](../search_problems.py) or one of its subclasses. The
arguments will be instances of `PositionSearchProblem` (collecting a single
bird) or `MultiplePositionSearchProblem` (collecting all the birds).

It would be good that you get familiar with the classes in the
[module](../search_problems.py), but all of the methods you will need to use
are listed later in this section.

States are described in the [previous section](1_getting_started.md). Here we
give more details on how these are implemented:

- For `PositionSearchProblem`, states are **pairs of integers**
    ```c
    (int, int)
    ```
    representing the coordinates of the red agent.

- For `MultiplePositionSearchProblem`, states are **nested** tuples
    ```c
    ((int, int), ((int, int), ...))
    ```
    where the first sub-tuple represents the coordinates of the red agent, the
    second sub-tuple is the set of coordinates of the remaining (yet to be
    collected) yellow birds.

What is important is that in either case the states are **hashable**

> An object is hashable if it has a hash value which never changes during its
> lifetime (it needs a `__hash__()` method), and can be compared to other
> objects (it needs an `__eq__()` method). When comparing, objects which are
> equal must have the same hash value.
>
> Hashability makes an object usable as a dictionary key and a set member,
> because these data structures use the hash value internally.
>
> All of Python's immutable built-in objects are hashable, while no mutable
> container (such as lists or dictionaries) is. Objects that are instances of
> user-defined classes are hashable by default; they all compare unequal
> (except with themselves), and their hash value is derived from their id().

so they can be put into a
[set](https://docs.python.org/3/tutorial/datastructures.html#sets) or used as
a key in a
[dictionary](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)
if your algorithms require it.

The typical interactions with instances of  ```SearchProblem``` or its
sub-classes will probably be:

- Obtaining the *initial state* via

    ```python
    s0 = problem.get_initial_state()
    ```

    or similar, so the variable ```s0``` contains a reference to the initial state.

- Test if a given state _s_ is a *goal* state or not, as in

    ```python
    if problem.goal_test(s):
        print("YAY!")
    else:
        print(":'(")
    ```

- Obtain the set of successors of a given state _s_ as in

    ```python
        for successor, action, cost in problem.get_successors(s) :
            ...
    ```

    where ```get_successors()``` allows you to iterate over a list of tuples with elements:

      - *successor* is a successor to the current state,
      - *action* is the action required to get there from state _s_,
      - and *cost* is the cost of doing the action on state _s_.

Efficient search techniques revolve around the idea of exploring the state
space in an intelligent manner, avoiding the need of revisiting the same state
multiple times. Each state is encapulated in a node containing the basic
information to reconstruct the path that starting from the initial state lead
to that state. In particular we suggest you to use the *SearchNode* class
[here](../search_strategies.py), which contains the following attributes:

- The _state_ visited at that step,
- a reference to the _parent_ node,
- the _action_ done on the state in the parent node leading to the current
  state,
- other data, depending on the algorithm. This data usually includes:
    - the accumulated cost *g(n)*, that is the sum of the costs of the actions
      done to reach _state_,
    - the value of one or more heuristics *h(n)*, providing estimates on the
      cost to get to a *goal* state,
    - the evaluation function *f(n)* combining actual and estimated costs *f(n)
      = g(n) + h(n)*.


As you have seen in the lecture, a search algorithm makes use of a data
structure representing the frontier of your search problem. Depending on how
you explore this frontier, i.e., the order in which you pick the next element
to be explored, you have a different search strategy. For this reason, we
provide you with different kinds of [frontiers](../frontiers.py).

Some algorithms require you to keep track of the parts already explored, that
aren't to be considered for exploration. This is usually called the **closed
list**; in order to have reasonable efficiency, it is implemented as a hash
table.

In order to help you, and also to help with grading, we provide you with a
readily available implementation of this data structure via the class
`SearchNode` in [search_strategies.py](../search_strategies.py).

## Adversarial Search Problems

Like all other agents, `MinimaxAgent` has a `get_action` method. This method
creates an instance of an `AdversarialSearchProblem`. Feel free to look at this
class in [search_problems.py](../search_problems.py), but we have
described all of the information which you need below.

In this problem, states are represented as the following tuple:

```python
(player, red_pos, black_pos, yellow_birds, score, yb_value)
```

where:
- `player` is an integer indicating the index of the current player. This is
   the player whose turn it is to play in this state (_0_ for red, _1_ for
   black),
- `red_pos` is a pair _(x,y)_ of integers specifying the red bird's position,
- `black_pos` is a pair _(x,y)_ of integers specifying the black bird's
  position,
- `yellow_birds` is a tuple of pairs specifying the positions of the remaining
  yellow birds,
- `score` is the current score reported by the UI, that is, the sum of the
  values of the yellow birds collected by red minus the values of those
  collected by black,
- `yb_value` is the value of a yellow bird, decreases at a constant rate after
  each player takes its turn.

The interface of the class `AdversarialSearchProblem` provides you with methods
to access potentially useful information:

- To obtain the index of the *maximizing* player you can do

    ```python
    max_player_id = problem.get_maximizing_player()
    ```

- If you need to know the index of the opponent player in the given state _s_

    ```Python
    opp_player_id = problem.opponent(s)
    ```

- To obtain the utility (score) of a given state _s_

    ```python
    value = problem.utility(s)
    ```

- To check if the given state _s_ is *terminal*

    ```python
    if problem.terminal_test(s) :
        print("GAME OVER")
    ```

- To iterate over the successors of a given state _s_ you can use the following

    ```python
    for next_state, action, _ in problem.get_successors(s) :
        # do something interesting with next_state
    ```

    note that agents can move onto the other agent position (triggering a
    capture and the end of the game). They cannot stay still (the action _STOP_
    is a special value only usable at the terminal).

- The width and height of the maze can be obtained via

    ```python
    w = problem.get_width()
    h = problem.get_height()
    ```

- The walls in the maze are stored as a matrix of Boolean values which you can access in
  a variety of ways, for instance

    ```python
    for i in range(h) :
        for j in range(w) :
            if problem.get_walls()[i][j] :
                print("CLONK!")
    ```

- If you need to obtain the **exact** distance between any two cells _p1_ and
  _p2_ you can get them through the method `maze_distance`

    ```python
    d_to_opponent =  problem.maze_distance(red_pos, black_pos)
    ```

That's all, you can now move to the [next section](3_breadth_first_search.md)
or go back to the [index](README.md).
