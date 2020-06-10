import nose
from a3_functions import make_recommendations

person_to_friends = {'Jay Pritchett': ['Gloria Pritchett', 'Manny Delgado', \
'Claire Dunphy'], 'Claire Dunphy': ['Phil Dunphy', 'Mitchell Pritchett', \
'Jay Pritchett'], 'Manny Delgado': ['Gloria Pritchett', 'Jay Pritchett', \
'Luke Dunphy'], 'Mitchell Pritchett': ['Claire Dunphy', 'Cameron Tucker', \
'Luke Dunphy'], 'Alex Dunphy': ['Luke Dunphy'], 'Cameron Tucker': \
['Mitchell Pritchett', 'Gloria Pritchett'], 'Haley Gwendolyn Dunphy': \
['Dylan D-Money'], 'Phil Dunphy': ['Claire Dunphy', 'Luke Dunphy'], \
'Dylan D-Money': ['Haley Gwendolyn Dunphy'], 'Gloria Pritchett': \
['Jay Pritchett', 'Cameron Tucker', 'Manny Delgado'], 'Luke Dunphy': \
['Manny Delgado', 'Alex Dunphy', 'Phil Dunphy', 'Mitchell Pritchett']}

person_to_networks = {'Phil Dunphy': ['Real Estate Association'], \
'Claire Dunphy': ['Parent Teacher Association'], 'Manny Delgado': \
['Chess Club'], 'Mitchell Pritchett': ['Law Association'], 'Alex Dunphy': \
['Orchestra', 'Chess Club'], 'Cameron Tucker': ['Clown School', \
'Wizard of Oz Fan Club'], 'Gloria Pritchett': ['Parent Teacher Association']}

# Rule 1: for every mutual friend that the person and the potential
# friend have, add 1 point to the potential friend's score.

# Rule 2: for each network that the person and the potential friend both
# belong to, add 1 point to the potential friend's score.

# Rule 3: MUST FOLLOW RULE 1 or 2 then if the person has
# the same last name as a potential friend who was identified through
# one or both of the previous two methods,
# add 1 point to the potential friend's score.


def test_nobody():
    '''Test someone who is not in this system.'''

    assert make_recommendations('Zedong Mao', person_to_friends, \
    person_to_networks) == []


def test_no_score():
    '''Test someone who has potential friends but gains no points
    through rule 1 and 2, hence no points gained from rule 3.'''

    assert make_recommendations('Haley Gwendolyn Dunphy', \
    person_to_friends, person_to_networks) == []


def test_score_through_rule_one():
    '''Test someone who gets points only through rule one.'''

    assert make_recommendations('Cameron Tucker', person_to_friends, \
    person_to_networks).sort() == [('Jay Pritchett', 1), ('Claire Dunphy', \
    1), ('Manny Delgado', 1), ('Luke Dunphy', 1)].sort()


def test_score_through_rule_two():
    '''Test someone who gets points only through rule two.'''

    test_friends_1 = {'Benjamin Bennie': ['Cox Cleverly'], 'Zipper Zoo': \
    ['Yeti Yeepman']}
    test_networks_1 = {'Benjamin Bennie': ['Joking Firm'], 'Zipper Zoo': \
    ['Joking Firm']}

    assert make_recommendations('Benjamin Bennie', test_friends_1, \
    test_networks_1).sort() == [('Zipper Zoo', 1)].sort()


def test_score_through_rule_one_and_three():
    '''Test someone who gets points both through rule one and three.'''

    test_friends_2 = {'Benjamin Bennie': ['Cox Cleverly'], 'Zipper Bennie': \
    ['Cox Cleverly']}
    test_networks_2 = {'Benjamin Bennie': ['Joking Firm'], 'Zipper Bennie': \
    ['Serious Firm']}

    assert make_recommendations('Benjamin Bennie', test_friends_2, \
    test_networks_2).sort() == [('Zipper Bennie', 2)].sort()


def test_score_through_rule_two_and_three():
    '''Test someone who gets points both through rule two and three.'''

    test_friends_3 = {'Benjamin Zoo': ['Cox Cleverly'], 'Zipper Zoo': \
    ['Yeti Yeepman']}
    test_networks_3 = {'Benjamin Zoo': ['Joking Firm'], 'Zipper Zoo': \
    ['Joking Firm']}

    assert make_recommendations('Benjamin Zoo', test_friends_3, \
    test_networks_3).sort() == [('Zipper Zoo', 2)].sort()


def test_score_through_rule_one_and_two():
    '''Test someone who gets points through only rule one and rule two.'''

    assert make_recommendations('Manny Delgado', person_to_friends, \
    person_to_networks).sort() == [('Claire Dunphy', 1), ('Mitchell \
    Pritchett', 1), ('Alex Dunphy', 2), ('Cameron Tucker', 1), ('Phil \
    Dunphy', 1)].sort()


def test_score_through_rule_one_two_and_three():
    '''Test someone who gets points through all of three rules.'''

    assert make_recommendations('Alex Dunphy', person_to_friends, \
    person_to_networks).sort() == [('Manny Delgado', 2), ('Mitchell \
    Pritchett', 1), ('Phil Dunphy', 2)].sort()


if __name__ == '__main__':
    nose.runmodule()
