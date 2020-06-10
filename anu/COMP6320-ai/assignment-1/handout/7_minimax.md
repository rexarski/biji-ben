# Question 5: Minimax
## _The Optimal Strategy (15 Marks)_

Implement Minimax in the methods `maximize()` and `minimize()` of the class
`MinimaxAgent` in [minimax_agent.py](../minimax_agent.py). This agent will be
tested over the Adversarial Search problem discussed in the
[Getting Started](1_getting_started.md) section. In the section
[Implementing Search Algorithms: The Fundamentals](2_implementation_notes.md)
you will find useful information meant to guide yourself through the code.

Your implementation of Minimax needs to have **all** of the following
properties:

1. Recursion on `maximize()` and `minimize()` stops whenever

    ```python
    current_depth == self.depth
    ```

2. Your Minimax implementation, when tested against the random black agent on
    the map `testAdversarial.lay` with the following command
    ```
    python3 red_bird.py -q -p MinimaxAgent -l adv_search_layouts/testAdversarial.lay -a depth=8 -n 100
    ```
    should obtain a `Win Rate` above `90/100`. One of our runs was like this
    ```
    Average Score: 510.92330307022235
    Scores:        393.0553130158992, 640.168281791879, 389.3826036510718, 654.0133882182124, 463.73655956431503, 449.2849260199849, 633.1542657003669, 626.5986929834296, -154.75687164529063, 616.2562372818809, 960.5989185816841, 633.656098393401, 793.422346452157, 789.598981242856, 789.598981242856, 449.10850870340664, 619.0280475324927, 279.8277144108473, 488.8183780786116, 460.9438214731905, 789.598981242856, 793.422346452157, 471.00889137760964, 456.5581110052495, 804.0120188592973, 445.99660882888077, 456.8012944804881, 465.3320968421789, -61.55033685459162, 615.6729641827283, 620.079602491182, 472.6789995322821, 396.583302977642, 619.0280475324927, 644.178330236238, 626.5986929834296, 615.6729641827283, 629.8327331841, 793.422346452157, 797.0950558169843, 460.2787766028109, 99.80222259125287, 460.2787766028109, 445.75342535364217, 633.8710247967242, 469.89046433765907, 460.38147621455056, 276.21062929402234, 636.344916582578, 449.53660387203615, 647.5673033168082, 456.1659141133781, -154.75687164529063, -154.75687164529063, 797.0950558169843, 810.3946098081457, -61.55033685459162, 393.0553130158992, 466.13522091048264, 283.2854973723514, 456.13236327988056, 807.2674528784904, 647.5673033168082, 789.598981242856, 629.8327331841, 789.598981242856, 469.07937708381473, -154.75687164529063, 452.81083076361364, 283.87036990004145, 640.8567977199712, 630.1983154318968, 460.7068717714403, 633.1542657003669, 618.8277220796049, 619.0280475324927, 287.39835986178423, 470.2921322812523, 456.13236327988056, 283.9730695117811, 640.6503402744952, 647.5673033168082, 276.29972444910453, 396.583302977642, 461.09403336834674, 456.7174131605704, 626.5986929834296, 449.10850870340664, 960.5989185816841, 283.87036990004145, 640.168281791879, 487.9805702400301, 472.9027422931158, 287.2946020280479, 807.2674528784904, 793.422346452157, 463.44340277316576, 460.3133544324259, 453.5672542798177, 452.81083076361364
    Win Rate:      94/100 (0.94)
    Record:        Win, Win, Win, Win, Win, Win, Win, Win, Loss, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Loss, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Loss, Loss, Win, Win, Loss, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Loss, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win, Win
    ```
    Note that the above is **indicative**. The random black agent, by its nature, can change its moves from match to match.

3. When tested against the greedy black agent on the same map with the command
    ```
    $ python3 red_bird.py -p MinimaxAgent -l adv_search_layouts/testAdversarial.lay -a depth=12 -n 3 -b GreedyBlackBirdAgent
    ```
    attains a performance against the black Agent similar or better than shown below
    ```
    The game is over. Score: -59.434305398668826
    Average Score: -59.43430539866883
    Scores:        -59.434305398668826, -59.434305398668826, -59.434305398668826
    Win Rate:      0/3 (0.00)
    Record:        Loss, Loss, Loss
    ```
    Note that the Greedy black agent is **deterministic** - it will be always taking the same move for any given game state.

4. Implement alpha-beta pruning to make your algorithm more efficient.

Let's take the Minimax agent out of its comfort zone, and deploy it on a
different maze
```
python3 red_bird.py -p MinimaxAgent -l adv_search_layouts/aiAdversarial.lay -a depth=4 -b GreedyBlackBirdAgent
```

Did the red agent manage to achieve anything? Now increase the depth a bit, say:
```
python3 red_bird.py -p MinimaxAgent -l adv_search_layouts/aiAdversarial.lay -a depth=6 -b GreedyBlackBirdAgent
```

Is the behavior you're observing a *bug* or a *feature*? Why is this happening?
You will need to understand what is going here in order to come up with a good
solution for the next question.

### Hints and Notes

1. When implementing the maximize and minimize methods, when we say "depth" in
   the code we actually refer to the number of minimizing and maximizing steps.
   Therefore, setting the depth to _4_ means that the game tree is going to be
   explored _2_ ply deep.
2. When the `maximize()` method hits a *terminal* state or the *depth cutoff*
   the action to be returned needs to be `Directions.STOP`. Check the
   definition of the class `Directions` in [actions.py](../actions.py).
3. The depth of a tree is the number of edges on the longest (direct) path from
   the root node to a leaf.
4. Don't change the evaluation function just yet (that's the next question).
5. Consider implementing minimax without alpha-beta pruning first. Then comment
   out this code and implement minimax with alpha-beta pruning. This way, in
   case your alpha-beta pruning impementation is incorrect, you can still get
   partial marks for the basic version.

Once you've finished, you can move to the
[next section](8_evaluation_function.md) or go back to the [index](README.md).
