
import agents
import minimax_agent
from game_rules import ClassicGameRules


def load_layout(infile='-'):
    import fileinput
    from layout import Layout

    buffer = []
    for line in fileinput.input():
        buffer.append(line.strip())

    return Layout(buffer)


def main():
    import text_display
    import random

    # Setup things so we can call the planner

    random.seed('comp3620_6320_2016')  # set RNG

    layout = load_layout()  # read stdin

    display = text_display.NullGraphics()  # disable graphics

    catch_exceptions = False  # abort program on exception

    timeout = 60  # time out

    # Agents setup
    red_bird = agents.SearchAgent(
        0, fn='depth_first_search', prob='PositionSearchProblem', heuristic='blind_heuristic')
    black_bird = None

    rules = ClassicGameRules(timeout)
    game = rules.new_game(layout, red_bird, black_bird,
                          display, False, catch_exceptions)
    game.solve()


if __name__ == '__main__':
    main()
