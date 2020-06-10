# game.py
# --------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course

""" This file defines the game class, which manages the control of the game. It
    gets actions from the agents and executes them until the game ends.

    ********** YOU SHOULD NOT CHANGE ANYTHING IN THIS FILE **********
"""

import os
import sys
import time
import traceback

import util
from util import TimeoutFunction, TimeoutFunctionException


class InvalidPlan(Exception):
    def __init__(self, plan, index):
        self.plan = plan
        self.index = index

    def __str__(self):
        message = ['The plan was invalid: an action was not applicable']
        message += ['Failing action: {} Index: {}'.format(
            self.plan[self.index], self.index)]
        message += ['Applicable prefix:']
        message += ['\t{}'.format(a) for a in self.plan[:self.index]]
        return '\n'.join(message)


class Game:
    """ The Game manages the control flow, soliciting actions from agents. """

    def __init__(self, red_bird_agent, black_bird_agent, display, rules,
                 starting_index=0, mute_agents=False, catch_exceptions=False):
        """ Make a new game with the given agents, display and rules.
            (Game, Agent, Agent, GedBirdGraphics/NullGraphics, ClassicGameRules,
                int, bool, bool) -> None
        """
        self.agent_crashed = False
        self.red_bird_agent = red_bird_agent
        self.black_bird_agent = black_bird_agent
        if black_bird_agent is not None:
            self.agents = [red_bird_agent, black_bird_agent]
        else:
            self.agents = [red_bird_agent]
        self.display = display
        self.rules = rules
        self.starting_index = starting_index
        self.game_over = False
        self.mute_agents = mute_agents
        self.catch_exceptions = catch_exceptions
        self.move_history = []
        self.total_agent_times = [0] * len(self.agents)
        self.total_agent_time_warnings = [0] * len(self.agents)
        self.agent_timeout = False
        import io
        self.agent_output = [io.StringIO() for agent in self.agents]

    def get_progress(self):
        """ Return the progress of the game (how many yellow birds are left).
            (Game) -> float
        """
        if self.game_over:
            return 1.0
        else:
            return self.rules.get_progress(self)

    def _agent_crash(self, agent_index, quiet=False):
        """ Helper method for handling agent crashes
            (Game, int, bool) -> None
        """
        if not quiet:
            traceback.print_exc()
        self.game_over = True
        self.agent_crashed = True
        self.rules.agent_crash(self, agent_index)

    OLD_STDOUT = None
    OLD_STDERR = None

    def mute(self, agent_index):
        """ Stop an agent from producing output.
            (Game, int) -> None
        """
        if not self.mute_agents:
            return
        global OLD_STDOUT, OLD_STDERR
        import io
        OLD_STDOUT = sys.stdout
        OLD_STDERR = sys.stderr
        sys.stdout = self.agent_output[agent_index]
        sys.stderr = self.agent_output[agent_index]

    def unmute(self):
        """ Allow an agent to produce output again.
            (Game, int) -> None
        """
        if not self.mute_agents:
            return
        global OLD_STDOUT, OLD_STDERR
        # Revert stdout/stderr to originals
        sys.stdout = OLD_STDOUT
        sys.stderr = OLD_STDERR

    def solve(self):
        import json
        agent = self.agents[0]
        self.mute(0)
        agent.register_initial_state(self.state.deepcopy())
        self.unmute()
        return agent.result
        # print((json.dumps(agent.result, sort_keys=True,indent=4)))

    def validate(self, plan):
        for i in range(0, len(plan)):
            try:
                self.state = self.state.successor(0, plan[i])
            except Exception as e:
                if 'Illegal action' in str(e):
                    raise InvalidPlan(plan, i)

    def run(self):
        """ Main control loop for game play.
            (Game) -> None
        """
        self.display.initialise(self.state)
        self.num_moves = 0
        for i in range(len(self.agents)):
            agent = self.agents[i]
            if not agent:
                self.mute(i)
                # this is a null agent, meaning it failed to load, the other team wins
                print("Agent %d failed to load" % i, file=sys.stderr)
                self.unmute()
                self._agent_crash(i, quiet=True)
                return
            if ("register_initial_state" in dir(agent)):
                self.mute(i)
                if self.catch_exceptions:
                    try:
                        timed_func = TimeoutFunction(agent.register_initial_state,
                                                     int(self.rules.getMaxStartupTime(i)))
                        try:
                            start_time = time.time()
                            timed_func(self.state.deepcopy())
                            time_taken = time.time() - start_time
                            self.total_agent_times[i] += time_taken
                        except TimeoutFunctionException:
                            print("Agent %d ran out of time on startup!" %
                                  i, file=sys.stderr)
                            self.unmute()
                            self.agent_timeout = True
                            self._agent_crash(i, quiet=True)
                            return
                    except Exception as data:
                        self._agent_crash(i, quiet=False)
                        self.unmute()
                        return
                else:
                    agent.register_initial_state(self.state.deepcopy())
                # TODO: could this exceed the total time
                self.unmute()

        agent_index = self.starting_index
        num_agents = len(self.agents)

        while not self.game_over:
            # Fetch the next agent
            agent = self.agents[agent_index]
            move_time = 0
            skip_action = False
            # Generate an observation of the state
            if 'observation_function' in dir(agent):
                self.mute(agent_index)
                if self.catch_exceptions:
                    try:
                        timed_func = TimeoutFunction(agent.observation_function,
                                                     int(self.rules.get_move_timeout(agent_index)))
                        try:
                            start_time = time.time()
                            observation = timed_func(self.state.deepcopy())
                        except TimeoutFunctionException:
                            skip_action = True
                        move_time += time.time() - start_time
                        self.unmute()
                    except Exception as data:
                        self._agent_crash(agent_index, quiet=False)
                        self.unmute()
                        return
                else:
                    observation = agent.observation_function(
                        self.state.deepcopy())
                self.unmute()
            else:
                observation = self.state.deepcopy()

            # Solicit an action
            action = None
            self.mute(agent_index)
            if self.catch_exceptions:
                try:
                    timed_func = TimeoutFunction(agent.get_action,
                                                 int(self.rules.get_move_timeout(agent_index)) - int(move_time))
                    try:
                        start_time = time.time()
                        if skip_action:
                            raise TimeoutFunctionException()
                        action = timed_func(observation)
                    except TimeoutFunctionException:
                        print("Agent %d timed out on a single move!" %
                              agent_index, file=sys.stderr)
                        self.agent_timeout = True
                        self._agent_crash(agent_index, quiet=True)
                        self.unmute()
                        return

                    move_time += time.time() - start_time

                    if move_time > self.rules.get_move_warning_time(agent_index):
                        self.total_agent_time_warnings[agent_index] += 1
                        print("Agent %d took too long to make a move! This is warning %d" %
                              (agent_index, self.total_agent_time_warnings[agent_index]), file=sys.stderr)
                        if self.total_agent_time_warnings[agent_index] > self.rules.get_max_time_warnings(agent_index):
                            print("Agent %d exceeded the maximum number of warnings: %d" %
                                  (agent_index, self.total_agent_time_warnings[agent_index]), file=sys.stderr)
                            self.agent_timeout = True
                            self._agent_crash(agent_index, quiet=True)
                            self.unmute()
                            return

                    self.total_agent_times[agent_index] += move_time
                    if self.total_agent_times[agent_index] > self.rules.get_max_total_time(agent_index):
                        print("Agent %d ran out of time! (time: %1.2f)" %
                              (agent_index, self.total_agent_times[agent_index]), file=sys.stderr)
                        self.agent_timeout = True
                        self._agent_crash(agent_index, quiet=True)
                        self.unmute()
                        return
                    self.unmute()
                except Exception as data:
                    self._agent_crash(agent_index)
                    self.unmute()
                    return
            else:
                action = agent.get_action(observation)
            self.unmute()

            # Execute the action
            self.move_history.append((agent_index, action))
            if self.catch_exceptions:
                try:
                    self.state = self.state.successor(agent_index, action)
                except Exception as data:
                    self.mute(agent_index)
                    self._agent_crash(agent_index)
                    self.unmute()
                    return
            else:
                self.state = self.state.successor(agent_index, action)

            # Change the display
            self.display.update(self.state, agent_index)

            # Allow for game specific conditions (winning, losing, etc.)
            self.rules.process(self.state, self)
            # Track progress
            if agent_index == num_agents + 1:
                self.num_moves += 1
            # Next agent
            agent_index = (agent_index + 1) % num_agents

        # inform a learning agent of the game result
        for agent_index, agent in enumerate(self.agents):
            if "final" in dir(agent):
                try:
                    self.mute(agent_index)
                    agent.final(self.state)
                    self.unmute()
                except Exception as data:
                    if not self.catch_exceptions:
                        raise
                    self._agent_crash(agent_index)
                    self.unmute()
                    return
        self.display.finish()
