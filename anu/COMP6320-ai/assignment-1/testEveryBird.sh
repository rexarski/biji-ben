#!/bin/sh

python3 red_bird.py -l search_layouts/$1.lay -p SearchAgent -a fn=astar,prob=MultiplePositionSearchProblem,heuristic=every_bird_heuristic
