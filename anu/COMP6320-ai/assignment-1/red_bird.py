# red_bird.py
# ----------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course

""" This is the main file of the program. It holds the logic for the classic
    red bird game along with the main code to run a game.

    There is nothing you really need to look at in this file.

    For those of you who really want to poke around, try:
        python red_bird.py --help

    to get the full command line arguments of the program.

    ********** YOU SHOULD NOT CHANGE ANYTHING IN THIS FILE **********
"""

import os
import random
import sys

import agents
import layout
import minimax_agent
from game_rules import ClassicGameRules

try:
    val = int(os.environ['PYTHONHASHSEED'])
except Exception as e:
    val = None

if val != 1:
    print('\n' + "*" * 80)
    print("- WARNING -\n Automatically setting PYTHONHASHSEED to 1 to obtain more reliable results")
    print("*" * 80 + '\n')
    # We simply set the environment variable and re-call ourselves.
    os.environ["PYTHONHASHSEED"] = '1'
    os.execv(sys.executable, [sys.executable] + sys.argv)
    sys.exit(1)


def default(arg):
    """ A function to prepare an argument string for a default argument.
        (str) -> str
    """
    return arg + ' [Default: %default]'


def parse_agent_args(args):
    """ Parse the arguments for an agent.
        (str) -> { str : str }
    """
    if not args:
        return {}
    pieces = args.split(',')
    opts = {}
    for p in pieces:
        if '=' in p:
            key, val = p.split('=')
        else:
            key, val = p, 1
        opts[key] = val
    return opts


def read_command():
    """ Processes the command used to run the program from the command line.
        ([str]) -> { str : object }
    """
    from argparse import ArgumentParser
    usage_str = """
    USAGE:      python red_bird.py <options>
    EXAMPLES:   (1) python red_bird.py -p MinimaxAgent -l anuAdversarial -a depth=4 -b GreedyBlackBirdAgent --frame_time 0.05
                        will start an adversarial game with your MinimaxAgent vs the GreedyBlackBirdAgent
                        on the anuAdversarial level
                (2) python red_bird.py -l anuAdversarial -p KeyboardAgent -b GreedyBlackBirdAgent
                        will allow you to play with the keyboard on the same level
    """
    parser = ArgumentParser(usage_str)

    parser.add_argument('-n', '--num_games', dest='num_games', type=int, action='store',
                        help='the number of GAMES to play', metavar='GAMES', default=1)
    parser.add_argument('-l', '--layout', dest='layout',
                        help='the LAYOUT_FILE from which to load the map layout (Mandatory)',
                        metavar='LAYOUT_FILE', default=None)
    parser.add_argument('-b', '--black_bird', dest='black_bird',
                        help='the black_bird agent TYPE in the agents module to use',
                        metavar='TYPE', default='BlackBirdAgent')
    parser.add_argument('-a', '--agent_args', dest='agent_args',
                        help='Comma separated values sent to agent. e.g. "opt1=val1,opt2,opt3=val3"')
    parser.add_argument('-p', '--red_bird', dest='red_bird',
                        help='the agent TYPE in the search_agents module to use',
                        metavar='TYPE', default='KeyboardAgent')
    parser.add_argument('-t', '--text_graphics', action='store_true', dest='text_graphics',
                        help='Display output as text only', default=False)
    parser.add_argument('-q', '--quiettext_graphics', action='store_true', dest='quiet_graphics',
                        help='Generate minimal output and no graphics', default=False)
    parser.add_argument('-z', '--zoom', type=float, dest='zoom',
                        help='Zoom the size of the graphics window', default=1.0)
    parser.add_argument('-f', '--fix_random_seed', action='store_true', dest='fix_random_seed',
                        help='Fixes the random seed to always play the same game', default=False)
    parser.add_argument('--frame_time', dest='frame_time', type=float,
                        help='Time to delay between frames; <0 means keyboard', default=0.1)
    parser.add_argument('-c', '--catch_exceptions', action='store_true', dest='catch_exceptions',
                        help='Turns on exception handling and timeouts during games', default=False)
    parser.add_argument('--timeout', dest='timeout', type=float,
                        help='Maximum length of time an agent can spend computing in a single game', default=30)

    options = parser.parse_args()
    args = dict()

    # Fix the random seed
    if options.fix_random_seed:
        random.seed('comp3620_6320_2016')

    # Choose a layout
    if options.layout is None:
        raise SystemExit("[Fatal]: No map layout was specified!")

    args['layout'] = layout.get_layout(options.layout)
    if args['layout'] == None:
        raise SystemExit("[Fatal]: Map layout " +
                         options.layout + " cannot be found")

    # Choose a red_bird agent
    no_keyboard = options.text_graphics or options.quiet_graphics
    red_bird_type = load_agent(options.red_bird, no_keyboard)
    agent_opts = parse_agent_args(options.agent_args)

    # Instantiate red_bird with agent_args
    red_bird = red_bird_type(0, **agent_opts)
    args['red_bird'] = red_bird

    # Choose a black_bird agent
    black_bird_type = load_agent(options.black_bird, no_keyboard)
    if args['layout'].has_black_bird():
        args['black_bird'] = black_bird_type(1)
    else:
        args['black_bird'] = None

    # Choose a display format
    if options.quiet_graphics:
        import text_display
        args['display'] = text_display.NullGraphics()
    elif options.text_graphics:
        import text_display
        text_display.SLEEP_TIME = options.frame_time
        args['display'] = text_display.RedBirdGraphics()
    else:
        import graphics_display
        args['display'] = graphics_display.RedBirdGraphics(options.zoom,
                                                           frame_time=options.frame_time)
    args['num_games'] = options.num_games
    args['catch_exceptions'] = options.catch_exceptions
    args['timeout'] = options.timeout

    return args


def load_agent(agent, no_graphics):
    """ Attempt to load the specified agent from agents.py.
        (str, bool) -> Agent
    """
    if no_graphics and agent == "KeyboardAgent":
        raise Exception(
            "Using the keyboard requires graphics (not text display)")
    if agent in dir(agents):
        return getattr(agents, agent)
    if agent in dir(minimax_agent):
        return getattr(minimax_agent, agent)
    raise Exception("The agent " + agent +
                    " is not specified in agents.py or minimax_agent.py.")


def run_games(layout, red_bird, black_bird, display, num_games, catch_exceptions=False,
              timeout=30):
    """ Run the given number of games with the specified layout, and agents.
        (Layout, Agent, Agent, RedBirdDisplay, int,  bool, number) -> [Game]
    """

    import __main__
    __main__.__dict__['_display'] = display

    rules = ClassicGameRules(timeout)
    games = []

    for _ in range(num_games):
        game = rules.new_game(layout, red_bird, black_bird,
                              display, False, catch_exceptions)
        game.run()
        games.append(game)

        # Restart agent
        red_bird.action_index = 0

    if num_games > 0:
        scores = [game.state.get_score() for game in games]
        wins = [game.state.score > 0 for game in games]
        win_rate = wins.count(True) / float(len(wins))
        print('Average Score:', sum(scores) / float(len(scores)))
        print('Scores:       ', ', '.join([str(score) for score in scores]))
        print('Win Rate:      %d/%d (%.2f)' %
              (wins.count(True), len(wins), win_rate))
        print('Record:       ', ', '.join(
            [['Loss', 'Win'][int(w)] for w in wins]))

    return games


if __name__ == '__main__':
    """
    The main function called when red_bird.py is run
    from the command line:

    > python red_bird.py

    See the usage string for more details.

    > python red_bird.py --help
    """

    args = read_command()  # Get game components based on input
    run_games(**args)
