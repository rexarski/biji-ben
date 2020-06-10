import nose
from a3_functions import load_profiles

person_to_friends = {'Jay Pritchett': ['Gloria Pritchett', 'Manny Delgado', \
'Claire Dunphy'], 'Claire Dunphy': ['Phil Dunphy', 'Mitchell Pritchett', \
'Jay Pritchett'], 'Manny Delgado': ['Gloria Pritchett', 'Jay Pritchett', \
'Luke Dunphy'], 'Mitchell Pritchett': ['Claire Dunphy', 'Cameron Tucker', \
'Luke Dunphy'], 'Alex Dunphy': ['Luke Dunphy'], 'Cameron Tucker': ['Mitchell \
Pritchett', 'Gloria Pritchett'], 'Haley Gwendolyn Dunphy': ['Dylan D-Money'], \
'Phil Dunphy': ['Claire Dunphy', 'Luke Dunphy'], 'Dylan D-Money': ['Haley \
Gwendolyn Dunphy'], 'Gloria Pritchett': ['Jay Pritchett', 'Cameron Tucker', \
'Manny Delgado'], 'Luke Dunphy': ['Manny Delgado', 'Alex Dunphy', 'Phil \
Dunphy', 'Mitchell Pritchett']}

person_to_networks = {'Phil Dunphy': ['Real Estate Association'], 'Claire \
Dunphy': ['Parent Teacher Association'], 'Manny Delgado': ['Chess Club'], \
'Mitchell Pritchett': ['Law Association'], 'Alex Dunphy': ['Orchestra', \
'Chess Club'], 'Cameron Tucker': ['Clown School', 'Wizard of Oz Fan Club'], \
'Gloria Pritchett': ['Parent Teacher Association']}

file_0 = open('file0.txt')
file_1 = open('file1.txt')
file_2 = open('file2.txt')
file_3 = open('file3.txt')
file_4 = open('file4.txt')
file_5 = open('file5.txt')
file_6 = open('file6.txt')


def test_empty():
    '''Test updating nothing.'''

    person_to_friends_test = {'Jay Pritchett': ['Gloria Pritchett', \
    'Manny Delgado', 'Claire Dunphy'], 'Claire Dunphy': ['Phil Dunphy', \
    'Mitchell Pritchett', 'Jay Pritchett'], 'Manny Delgado': \
    ['Gloria Pritchett', 'Jay Pritchett', 'Luke Dunphy'], \
    'Mitchell Pritchett': ['Claire Dunphy', 'Cameron Tucker', 'Luke Dunphy'], \
    'Alex Dunphy': ['Luke Dunphy'], 'Cameron Tucker': ['Mitchell Pritchett', \
    'Gloria Pritchett'], 'Haley Gwendolyn Dunphy': ['Dylan D-Money'], \
    'Phil Dunphy': ['Claire Dunphy', 'Luke Dunphy'], 'Dylan D-Money': \
    ['Haley Gwendolyn Dunphy'], 'Gloria Pritchett': ['Jay Pritchett', \
    'Cameron Tucker', 'Manny Delgado'], 'Luke Dunphy': ['Manny Delgado', \
    'Alex Dunphy', 'Phil Dunphy', 'Mitchell Pritchett']}

    person_to_networks_test = {'Phil Dunphy': ['Real Estate Association'], \
    'Claire Dunphy': ['Parent Teacher Association'], 'Manny Delgado': \
    ['Chess Club'], 'Mitchell Pritchett': ['Law Association'], 'Alex Dunphy': \
    ['Orchestra', 'Chess Club'], 'Cameron Tucker': ['Clown School', \
    'Wizard of Oz Fan Club'], 'Gloria Pritchett': \
    ['Parent Teacher Association']}

    load_profiles(file_0, person_to_friends_test, person_to_networks_test)

    assert person_to_friends_test == {'Jay Pritchett': ['Gloria Pritchett', \
    'Manny Delgado', 'Claire Dunphy'], 'Claire Dunphy': ['Phil Dunphy', \
    'Mitchell Pritchett', 'Jay Pritchett'], 'Manny Delgado': \
    ['Gloria Pritchett', 'Jay Pritchett', 'Luke Dunphy'], \
    'Mitchell Pritchett': ['Claire Dunphy', 'Cameron Tucker', \
    'Luke Dunphy'], 'Alex Dunphy': ['Luke Dunphy'], 'Cameron Tucker': \
    ['Mitchell Pritchett', 'Gloria Pritchett'], 'Haley Gwendolyn Dunphy': \
    ['Dylan D-Money'], 'Phil Dunphy': ['Claire Dunphy', 'Luke Dunphy'], \
    'Dylan D-Money': ['Haley Gwendolyn Dunphy'], 'Gloria Pritchett': \
    ['Jay Pritchett', 'Cameron Tucker', 'Manny Delgado'], 'Luke Dunphy': \
    ['Manny Delgado', 'Alex Dunphy', 'Phil Dunphy', 'Mitchell Pritchett']} \
    and person_to_networks_test == {'Phil Dunphy': \
    ['Real Estate Association'], 'Claire Dunphy': \
    ['Parent Teacher Association'], 'Manny Delgado': ['Chess Club'], \
    'Mitchell Pritchett': ['Law Association'], 'Alex Dunphy': ['Orchestra', \
    'Chess Club'], 'Cameron Tucker': ['Clown School', \
    'Wizard of Oz Fan Club'], 'Gloria Pritchett': \
    ['Parent Teacher Association']}


def test_first_new():
    '''Test adding new friend who is out of the existing social circle
    before.'''

    person_to_friends_test = {'Jay Pritchett': ['Gloria Pritchett', \
    'Manny Delgado', 'Claire Dunphy'], 'Claire Dunphy': ['Phil Dunphy', \
    'Mitchell Pritchett', 'Jay Pritchett'], 'Manny Delgado': \
    ['Gloria Pritchett', 'Jay Pritchett', 'Luke Dunphy'], \
    'Mitchell Pritchett': ['Claire Dunphy', 'Cameron Tucker', 'Luke Dunphy'], \
    'Alex Dunphy': ['Luke Dunphy'], 'Cameron Tucker': ['Mitchell Pritchett', \
    'Gloria Pritchett'], 'Haley Gwendolyn Dunphy': ['Dylan D-Money'], \
    'Phil Dunphy': ['Claire Dunphy', 'Luke Dunphy'], 'Dylan D-Money': \
    ['Haley Gwendolyn Dunphy'], 'Gloria Pritchett': ['Jay Pritchett', \
    'Cameron Tucker', 'Manny Delgado'], 'Luke Dunphy': ['Manny Delgado', \
    'Alex Dunphy', 'Phil Dunphy', 'Mitchell Pritchett']}

    person_to_networks_test = {'Phil Dunphy': ['Real Estate Association'], \
    'Claire Dunphy': ['Parent Teacher Association'], 'Manny Delgado': \
    ['Chess Club'], 'Mitchell Pritchett': ['Law Association'], 'Alex Dunphy': \
    ['Orchestra', 'Chess Club'], 'Cameron Tucker': ['Clown School', \
    'Wizard of Oz Fan Club'], 'Gloria Pritchett': \
    ['Parent Teacher Association']}

    load_profiles(file_1, person_to_friends_test, person_to_networks_test)

    assert person_to_friends_test == {'Jay Pritchett': ['Gloria Pritchett', \
    'Manny Delgado', 'Claire Dunphy'], 'Claire Dunphy': ['Phil Dunphy', \
    'Mitchell Pritchett', 'Jay Pritchett'], 'Manny Delgado': \
    ['Gloria Pritchett', 'Jay Pritchett', 'Luke Dunphy'], \
    'Mitchell Pritchett': ['Claire Dunphy', 'Cameron Tucker', 'Luke Dunphy'], \
    'Alex Dunphy': ['Luke Dunphy'], 'Cameron Tucker': ['Mitchell Pritchett', \
    'Gloria Pritchett'], 'Haley Gwendolyn Dunphy': ['Dylan D-Money'], \
    'Phil Dunphy': ['Claire Dunphy', 'Luke Dunphy', 'Fake Dunphy'], \
    'Dylan D-Money': ['Haley Gwendolyn Dunphy'], 'Gloria Pritchett': \
    ['Jay Pritchett', 'Cameron Tucker', 'Manny Delgado'], 'Luke Dunphy': \
    ['Manny Delgado', 'Alex Dunphy', 'Phil Dunphy', 'Mitchell Pritchett'], \
    'Fake Dunphy': ['Phil Dunphy']}


def test_new_between():
    '''Test adding new friendship between two persons who are
    previously in the social circle.'''

    person_to_friends_test = {'Jay Pritchett': ['Gloria Pritchett', \
    'Manny Delgado', 'Claire Dunphy'], 'Claire Dunphy': ['Phil Dunphy', \
    'Mitchell Pritchett', 'Jay Pritchett'], 'Manny Delgado': \
    ['Gloria Pritchett', 'Jay Pritchett', 'Luke Dunphy'], \
    'Mitchell Pritchett': ['Claire Dunphy', 'Cameron Tucker', 'Luke Dunphy'], \
    'Alex Dunphy': ['Luke Dunphy'], 'Cameron Tucker': ['Mitchell Pritchett', \
    'Gloria Pritchett'], 'Haley Gwendolyn Dunphy': ['Dylan D-Money'], \
    'Phil Dunphy': ['Claire Dunphy', 'Luke Dunphy'], 'Dylan D-Money': \
    ['Haley Gwendolyn Dunphy'], 'Gloria Pritchett': ['Jay Pritchett', \
    'Cameron Tucker', 'Manny Delgado'], 'Luke Dunphy': ['Manny Delgado', \
    'Alex Dunphy', 'Phil Dunphy', 'Mitchell Pritchett']}

    person_to_networks_test = {'Phil Dunphy': ['Real Estate Association'], \
    'Claire Dunphy': ['Parent Teacher Association'], 'Manny Delgado': \
    ['Chess Club'], 'Mitchell Pritchett': ['Law Association'], 'Alex Dunphy': \
    ['Orchestra', 'Chess Club'], 'Cameron Tucker': ['Clown School', \
    'Wizard of Oz Fan Club'], 'Gloria Pritchett': \
    ['Parent Teacher Association']}

    load_profiles(file_2, person_to_friends_test, person_to_networks_test)

    assert person_to_friends_test == {'Jay Pritchett': ['Gloria Pritchett', \
    'Manny Delgado', 'Claire Dunphy', 'Mitchell Pritchett'], 'Claire Dunphy': \
    ['Phil Dunphy', 'Mitchell Pritchett', 'Jay Pritchett'], 'Manny Delgado': \
    ['Gloria Pritchett', 'Jay Pritchett', 'Luke Dunphy'], \
    'Mitchell Pritchett': ['Claire Dunphy', 'Cameron Tucker', 'Luke Dunphy', \
    'Jay Pritchett'], 'Alex Dunphy': ['Luke Dunphy'], 'Cameron Tucker': \
    ['Mitchell Pritchett', 'Gloria Pritchett'], 'Haley Gwendolyn Dunphy': \
    ['Dylan D-Money'], 'Phil Dunphy': ['Claire Dunphy', 'Luke Dunphy'], \
    'Dylan D-Money': ['Haley Gwendolyn Dunphy'], 'Gloria Pritchett': \
    ['Jay Pritchett', 'Cameron Tucker', 'Manny Delgado'], 'Luke Dunphy': \
    ['Manny Delgado', 'Alex Dunphy', 'Phil Dunphy', 'Mitchell Pritchett']}


def test_add_network():
    '''Test to add a new network to somebody.'''

    person_to_friends_test = {'Jay Pritchett': ['Gloria Pritchett', \
    'Manny Delgado', 'Claire Dunphy'], 'Claire Dunphy': ['Phil Dunphy', \
    'Mitchell Pritchett', 'Jay Pritchett'], 'Manny Delgado': \
    ['Gloria Pritchett', 'Jay Pritchett', 'Luke Dunphy'], \
    'Mitchell Pritchett': ['Claire Dunphy', 'Cameron Tucker', 'Luke Dunphy'], \
    'Alex Dunphy': ['Luke Dunphy'], 'Cameron Tucker': ['Mitchell Pritchett', \
    'Gloria Pritchett'], 'Haley Gwendolyn Dunphy': ['Dylan D-Money'], \
    'Phil Dunphy': ['Claire Dunphy', 'Luke Dunphy'], 'Dylan D-Money': \
    ['Haley Gwendolyn Dunphy'], 'Gloria Pritchett': ['Jay Pritchett', \
    'Cameron Tucker', 'Manny Delgado'], 'Luke Dunphy': ['Manny Delgado', \
    'Alex Dunphy', 'Phil Dunphy', 'Mitchell Pritchett']}

    person_to_networks_test = {'Phil Dunphy': ['Real Estate Association'], \
    'Claire Dunphy': ['Parent Teacher Association'], 'Manny Delgado': \
    ['Chess Club'], 'Mitchell Pritchett': ['Law Association'], 'Alex Dunphy': \
    ['Orchestra', 'Chess Club'], 'Cameron Tucker': ['Clown School', \
    'Wizard of Oz Fan Club'], 'Gloria Pritchett': \
    ['Parent Teacher Association']}

    load_profiles(file_3, person_to_friends_test, person_to_networks_test)

    assert person_to_networks_test == {'Phil Dunphy': \
    ['Real Estate Association', 'Law Association'], 'Claire Dunphy': \
    ['Parent Teacher Association'], 'Manny Delgado': ['Chess Club'], \
    'Mitchell Pritchett': ['Law Association'], 'Alex Dunphy': ['Orchestra', \
    'Chess Club'], 'Cameron Tucker': ['Clown School', \
    'Wizard of Oz Fan Club'], 'Gloria Pritchett': \
    ['Parent Teacher Association']}


def test_add_alien():
    '''Test to add a new person without friends or networks.'''

    person_to_friends_test = {'Jay Pritchett': ['Gloria Pritchett', \
    'Manny Delgado', 'Claire Dunphy'], 'Claire Dunphy': ['Phil Dunphy', \
    'Mitchell Pritchett', 'Jay Pritchett'], 'Manny Delgado': \
    ['Gloria Pritchett', 'Jay Pritchett', 'Luke Dunphy'], \
    'Mitchell Pritchett': ['Claire Dunphy', 'Cameron Tucker', 'Luke Dunphy'], \
    'Alex Dunphy': ['Luke Dunphy'], 'Cameron Tucker': ['Mitchell Pritchett', \
    'Gloria Pritchett'], 'Haley Gwendolyn Dunphy': ['Dylan D-Money'], \
    'Phil Dunphy': ['Claire Dunphy', 'Luke Dunphy'], 'Dylan D-Money': \
    ['Haley Gwendolyn Dunphy'], 'Gloria Pritchett': ['Jay Pritchett', \
    'Cameron Tucker', 'Manny Delgado'], 'Luke Dunphy': ['Manny Delgado', \
    'Alex Dunphy', 'Phil Dunphy', 'Mitchell Pritchett']}

    person_to_networks_test = {'Phil Dunphy': ['Real Estate Association'], \
    'Claire Dunphy': ['Parent Teacher Association'], 'Manny Delgado': \
    ['Chess Club'], 'Mitchell Pritchett': ['Law Association'], 'Alex Dunphy': \
    ['Orchestra', 'Chess Club'], 'Cameron Tucker': ['Clown School', \
    'Wizard of Oz Fan Club'], 'Gloria Pritchett': \
    ['Parent Teacher Association']}

    load_profiles(file_4, person_to_friends_test, person_to_networks_test)

    assert  person_to_friends_test == {'Jay Pritchett': ['Gloria Pritchett', \
    'Manny Delgado', 'Claire Dunphy'], 'Claire Dunphy': ['Phil Dunphy', \
    'Mitchell Pritchett', 'Jay Pritchett'], 'Manny Delgado': \
    ['Gloria Pritchett', 'Jay Pritchett', 'Luke Dunphy'], \
    'Mitchell Pritchett': ['Claire Dunphy', 'Cameron Tucker', 'Luke Dunphy'], \
    'Alex Dunphy': ['Luke Dunphy'], 'Cameron Tucker': ['Mitchell Pritchett', \
    'Gloria Pritchett'], 'Haley Gwendolyn Dunphy': ['Dylan D-Money'], \
    'Phil Dunphy': ['Claire Dunphy', 'Luke Dunphy'], 'Dylan D-Money': \
    ['Haley Gwendolyn Dunphy'], 'Gloria Pritchett': ['Jay Pritchett', \
    'Cameron Tucker', 'Manny Delgado'], 'Luke Dunphy': ['Manny Delgado', \
    'Alex Dunphy', 'Phil Dunphy', 'Mitchell Pritchett']} and \
    person_to_networks_test == {'Phil Dunphy': ['Real Estate Association'], \
    'Claire Dunphy': ['Parent Teacher Association'], 'Manny Delgado': \
    ['Chess Club'], 'Mitchell Pritchett': ['Law Association'], \
    'Alex Dunphy': ['Orchestra', 'Chess Club'], 'Cameron Tucker': \
    ['Clown School', 'Wizard of Oz Fan Club'], 'Gloria Pritchett': \
    ['Parent Teacher Association']}


def test_add_networkless():
    '''Test to add a new person without networks.'''

    person_to_friends_test = {'Jay Pritchett': ['Gloria Pritchett', \
    'Manny Delgado', 'Claire Dunphy'], 'Claire Dunphy': ['Phil Dunphy', \
    'Mitchell Pritchett', 'Jay Pritchett'], 'Manny Delgado': \
    ['Gloria Pritchett', 'Jay Pritchett', 'Luke Dunphy'], \
    'Mitchell Pritchett': ['Claire Dunphy', 'Cameron Tucker', 'Luke Dunphy'], \
    'Alex Dunphy': ['Luke Dunphy'], 'Cameron Tucker': ['Mitchell Pritchett', \
    'Gloria Pritchett'], 'Haley Gwendolyn Dunphy': ['Dylan D-Money'], \
    'Phil Dunphy': ['Claire Dunphy', 'Luke Dunphy'], 'Dylan D-Money': \
    ['Haley Gwendolyn Dunphy'], 'Gloria Pritchett': ['Jay Pritchett', \
    'Cameron Tucker', 'Manny Delgado'], 'Luke Dunphy': ['Manny Delgado', \
    'Alex Dunphy', 'Phil Dunphy', 'Mitchell Pritchett']}

    person_to_networks_test = {'Phil Dunphy': ['Real Estate Association'], \
    'Claire Dunphy': ['Parent Teacher Association'], 'Manny Delgado': \
    ['Chess Club'], 'Mitchell Pritchett': ['Law Association'], 'Alex Dunphy': \
    ['Orchestra', 'Chess Club'], 'Cameron Tucker': ['Clown School', \
    'Wizard of Oz Fan Club'], 'Gloria Pritchett': \
    ['Parent Teacher Association']}

    load_profiles(file_5, person_to_friends_test, person_to_networks_test)

    assert  person_to_friends_test == {'Jay Pritchett': ['Gloria Pritchett', \
    'Manny Delgado', 'Claire Dunphy', 'Batman Batman'], 'Claire Dunphy': \
    ['Phil Dunphy', 'Mitchell Pritchett', 'Jay Pritchett'], 'Manny Delgado': \
    ['Gloria Pritchett', 'Jay Pritchett', 'Luke Dunphy'], \
    'Mitchell Pritchett': ['Claire Dunphy', 'Cameron Tucker', 'Luke Dunphy'], \
    'Alex Dunphy': ['Luke Dunphy'], 'Cameron Tucker': ['Mitchell Pritchett', \
    'Gloria Pritchett'], 'Haley Gwendolyn Dunphy': ['Dylan D-Money'], \
    'Phil Dunphy': ['Claire Dunphy', 'Luke Dunphy'], 'Dylan D-Money': \
    ['Haley Gwendolyn Dunphy'], 'Gloria Pritchett': ['Jay Pritchett', \
    'Cameron Tucker', 'Manny Delgado'], 'Luke Dunphy': ['Manny Delgado', \
    'Alex Dunphy', 'Phil Dunphy', 'Mitchell Pritchett'], 'Batman Batman': \
    ['Jay Pritchett']} and person_to_networks_test == {'Phil Dunphy': \
    ['Real Estate Association'], 'Claire Dunphy': \
    ['Parent Teacher Association'], 'Manny Delgado': ['Chess Club'], \
    'Mitchell Pritchett': ['Law Association'], 'Alex Dunphy': ['Orchestra', \
    'Chess Club'], 'Cameron Tucker': ['Clown School', \
    'Wizard of Oz Fan Club'], 'Gloria Pritchett': \
    ['Parent Teacher Association']}


def test_add_friendless():
    '''Test to add a new person without friends.'''

    person_to_friends_test = {'Jay Pritchett': ['Gloria Pritchett', \
    'Manny Delgado', 'Claire Dunphy'], 'Claire Dunphy': ['Phil Dunphy', \
    'Mitchell Pritchett', 'Jay Pritchett'], 'Manny Delgado': \
    ['Gloria Pritchett', 'Jay Pritchett', 'Luke Dunphy'], \
    'Mitchell Pritchett': ['Claire Dunphy', 'Cameron Tucker', 'Luke Dunphy'], \
    'Alex Dunphy': ['Luke Dunphy'], 'Cameron Tucker': ['Mitchell Pritchett', \
    'Gloria Pritchett'], 'Haley Gwendolyn Dunphy': ['Dylan D-Money'], \
    'Phil Dunphy': ['Claire Dunphy', 'Luke Dunphy'], 'Dylan D-Money': \
    ['Haley Gwendolyn Dunphy'], 'Gloria Pritchett': ['Jay Pritchett', \
    'Cameron Tucker', 'Manny Delgado'], 'Luke Dunphy': ['Manny Delgado', \
    'Alex Dunphy', 'Phil Dunphy', 'Mitchell Pritchett']}

    person_to_networks_test = {'Phil Dunphy': ['Real Estate Association'], \
    'Claire Dunphy': ['Parent Teacher Association'], 'Manny Delgado': \
    ['Chess Club'], 'Mitchell Pritchett': ['Law Association'], 'Alex Dunphy': \
    ['Orchestra', 'Chess Club'], 'Cameron Tucker': ['Clown School', \
    'Wizard of Oz Fan Club'], 'Gloria Pritchett': \
    ['Parent Teacher Association']}

    load_profiles(file_6, person_to_friends_test, person_to_networks_test)
    assert  person_to_friends_test == {'Jay Pritchett': ['Gloria Pritchett', \
    'Manny Delgado', 'Claire Dunphy'], 'Claire Dunphy': ['Phil Dunphy', \
    'Mitchell Pritchett', 'Jay Pritchett'], 'Manny Delgado': \
    ['Gloria Pritchett', 'Jay Pritchett', 'Luke Dunphy'], \
    'Mitchell Pritchett': ['Claire Dunphy', 'Cameron Tucker', 'Luke Dunphy'], \
    'Alex Dunphy': ['Luke Dunphy'], 'Cameron Tucker': ['Mitchell Pritchett', \
    'Gloria Pritchett'], 'Haley Gwendolyn Dunphy': ['Dylan D-Money'], \
    'Phil Dunphy': ['Claire Dunphy', 'Luke Dunphy'], 'Dylan D-Money': \
    ['Haley Gwendolyn Dunphy'], 'Gloria Pritchett': ['Jay Pritchett', \
    'Cameron Tucker', 'Manny Delgado'], 'Luke Dunphy': ['Manny Delgado', \
    'Alex Dunphy', 'Phil Dunphy', \
    'Mitchell Pritchett']} and person_to_networks_test == {'Phil Dunphy': \
    ['Real Estate Association'], 'Claire Dunphy': \
    ['Parent Teacher Association'], 'Manny Delgado': ['Chess Club'], \
    'Mitchell Pritchett': ['Law Association'], 'Alex Dunphy': \
    ['Orchestra', 'Chess Club'], 'Cameron Tucker': ['Clown School', \
    'Wizard of Oz Fan Club'], 'Gloria Pritchett': \
    ['Parent Teacher Association'], 'Batman Batman': ['Comics Company']}


if __name__ == '__main__':
    nose.runmodule()
