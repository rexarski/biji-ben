# Question 4: Developing Heuristics
## _Dealing with Multiple Goals_ (20 Marks)

Now the red bird has to collect all the yellow birds on the map! First, we will
take a look at the performance of A* with the _null heuristic_ `h(s)=0`
(**Note:** in this case A* becomes the Uniform Cost strategy). Then, you will
start with a *very simple* heuristic that captures the essence of the task
(picking up yellow birds), but already significantly improves the runtime of
A*. Finally, you will move onto a more powerful heuristic.

Each of the two latter heuristics will need to be implemented inside the file
[heuristics.py](../heuristics.py)

### The Baseline Heuristic

Let's first assess how well the null heuristic handles the navigation problem
with constraints. With this command
```
python3 red_bird.py -l search_layouts/<map> -p SearchAgent -a fn=astar,prob=MultiplePositionSearchProblem,heuristic=null
```
you can run your implementation of A* with the _null heuristic_ over the
instances of the following harder layouts:

- `aiMultiSearch.lay`
- `anuMultiSearch.lay`
- `smallMultiSearch.lay`
- `mazeMultiSearch.lay`

If you're using Mac or Linux, you can run these shortcuts instead:

```sh
./testEveryBirdNull.sh aiMultiSearch
./testEveryBirdNull.sh anuMultiSearch
./testEveryBirdNull.sh smallMultiSearch
./testEveryBirdNull.sh mazeMultiSearch
```

On our test machine, we get the following results with our implementation of A*:

Problem | Cost | Expanded Nodes | Time (secs)
--------|------|----------------|-----
aiMultiSearch | 55 | 6,633 | 0.1
anuMultiSearch | 99 | 13,912 | 0.1
smallMultiSearch | 60| 16,688 | 0.2
mazeMultiSearch | 215  | 534,496 | 7.8


### Counting Birds (5 Marks)

The first admissible heuristic we will consider is given by the following formula:

```
h(s) = number_of_yellow_birds_still_to_be_captured
```

Implement the above in the function `bird_counting_heuristic()` in the file
[heuristics.py](../heuristics.py).

You can see the effect of using this heuristic with the following command:

```
python3 red_bird.py -l search_layouts/<map> -p SearchAgent -a fn=astar,prob=MultiplePositionSearchProblem,heuristic=bch
```

Verify that your heuristic works correctly (it needs to be _0_ for *goal states*)
and also comparing with the tables below for A*:

Problem | Cost | Expanded Nodes | Time (secs)
--------|------|----------------|-----
aiMultiSearch | 55 | 6,092 | 0.1
anuMultiSearch | 99 | 13,502 | 0.2
smallMultiSearch | 60 | 12,517  | 0.1
mazeMultiSearch | 215 | 485,961 | 7.1

This heuristic is indeed **admissible** but it is still not very
**informative** because it completely abstracts the navigation problem away.
The effect of this becomes stronger on the larger problems.

### Come up with your heuristic! (15 Marks)

In this exercise you are requested to devise a much **more informative
admissible** heuristic for the problem. This heuristic will be graded according
to different factors:

1. Admissibility: your heuristic value must not exceed the smaller number of
   steps to collect all yellow birds.
2. Informativeness: measured by the reduction of Expanded Nodes w.r.t. the
   counting Birds heuristic.
3. Efficiency: reduction of run time.

You can see the effect of your implementation with the following command:

```
python3 red_bird.py -l search_layouts/<map> -p SearchAgent -a fn=astar,prob=MultiplePositionSearchProblem,heuristic=every_bird
```

If you're using Mac or Linux, you can run these shortcuts instead:

```sh
./testEveryBird.sh aiMultiSearch
./testEveryBird.sh anuMultiSearch
./testEveryBird.sh smallMultiSearch
./testEveryBird.sh mazeMultiSearch
```

Our current implementation achieves the following performance though you are
not required to compete with it. The reduction of number of expanded nodes and
overall time has to be done w.r.t. the counting birds heuristic presented
above. We expect to see substantial efficiency gains in the bigger instance
(i.e., mazeMultiSearch)

Problem | Cost | Expanded Nodes | Time (secs)
--------|------|----------------|-----
aiMultiSearch | 55 | 201 | 1.3
anuMultiSearch | 99| 308 | 0.7
smallMultiSearch | 60 | 410 | 0.9
mazeMultiSearch | 215| 702 | 1.0

Hints:

1. Your heuristic should not try to solve the original problem! It has to relax
   it to make it simpler so that the heuristic be efficiently computable. There
   is a tradeoff between efficiency and informativeness.
2. There are many ways to relax the problem (see lectures for examples).
3. The class `search_problems` contains a very interesting method that is
   called `maze_distance`. You may want to have a look into it.

Once you've finished, you can move to [the next section](7_minimax.md) or go
back to the [index](README.md).
