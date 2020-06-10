#!/bin/sh

python3 red_bird.py -p MinimaxAgent -l adv_search_layouts/$1.lay -a depth=${2} -b GreedyBlackBirdAgent --timeout 60 -c
