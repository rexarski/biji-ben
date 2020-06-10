# Question 6: Evaluation Functions for Two-Player Games (15 Marks)

Improve upon your Minimax agent by implementing a strong *evaluation function*
for this game. The evaluation function will be invoked when the search cannot
reach a terminal state within the given **depth limit**.

You need to implement your evaluation function in such a way that you can use
it within the method `evaluation()` of the class `MinimaxAgent` in
[minimax_agent.py](../minimax_agent.py). In addition, you will have to create
and include a text file called `eval_function.results.md` whose contents are
detailed below. There is no need to include your student ID in this file.

To give you an idea of what kinds of scores you should aim for, here are the
numbers achieved by our benchmark evaluation function. You don't have to
achieve these scores to get full marks. We will manually look at your code and
give marks based on originality, simplicity, and efficiency. Thus you'll need
to comment your code well so that the tutor can understand your method.

| Maze                  | Depth | Score |
| --------------------- | ----- | ----- |
| testAdversarial       | 12    | 89    |
| smallAdversarial      | 2     | 92    |
| aiAdversarial         | 10    | 86    |
| anuAdversarial        | 8     | -78   |
| mazeAdversarial       | 10    | -79   |
| smallDenseAdversarial | 6     | 253   |
| aiDenseAdversarial    | 6     | -504  |
| anuDenseAdversarial   | 6     | -579  |
| mazeDenseAdversarial  | 6     | 702   |

We need you to include in the file `eval_function.results.md` a table like the
one above, encoded using Markdown syntax (see the source of this file to see
how to do that), reporting your depths and scores. There is no need to
automatically generate this file. You can simply manually put your results into
the table of the md file.

You can do the tests with the following command:

```
python3 red_bird.py -p MinimaxAgent -l adv_search_layouts/<map>.lay -a depth=<d> -b GreedyBlackBirdAgent
```

where `<map>` is the map name, and `<d>` is the value for the depth.

Try to design evaluation functions where each of the above experiments can be
run within 60 seconds. This can be tested as follows:
```
python3 red_bird.py -p MinimaxAgent -l adv_search_layouts/<map>.lay -a depth=<d> -b GreedyBlackBirdAgent --timeout 60 -c
```

### Hints

1. The value that this function returns should reflect an estimate of the
   maximum score the red agent can attain from the given state. However, you
   might find this exercise difficult if you take that too literally.

2. Read carefully the section on Adversarial Search in the
   [Getting Started](1_getting_started.md) and [Implementation
   Notes](2_implementation_notes.md) sections.

3. The default implementation (see the implementation of `evaluation()` in
   `MinimaxAgent` for example) just returns the score of a given state. Think
   hard about the following: why did this (dummy) evaluation function work
   quite well on the test map?

4. You can greatly speed up the proceedings using the command line argument
   '-q', this kills the graphics.

5. Make sure your evaluation isn't too pessimistic. This can get you into
   trouble, since Minimax is built around the assumption that the MAX player is
   being realistic about its possibilities and possible winning strategies may
   be pruned away.

And that's it! You've completed the assignment :-)
