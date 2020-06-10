import nose
from a3_functions import invert_networks_dict

empty = {}
one_p_one_n = {'apple': ['A'], 'bike': ['B']}
one_p_mult_n = {'apple': ['a', 'A'], 'bike': ['b', 'B']}
mult_p_one_n = {'apple': ['A'], 'animal': ['A']}
mult_p_mult_n = {'apple': ['a', 'A'], 'animal': ['A'], 'bike': ['b', 'B']}
one_p_zero_n = {'apple': []}
mult_p_zero_n = {'apple': [], 'bike': []}


def test_empty():

    assert invert_networks_dict(empty) == {}


def test_one_person_one_network():

    assert invert_networks_dict(one_p_one_n) == \
    {'A': ['apple'], 'B': ['bike']}


def test_one_person_mult_network():

    assert invert_networks_dict(one_p_mult_n) == \
    {'a': ['apple'], 'A': ['apple'], 'b': ['bike'], 'B': ['bike']}


def test_mult_person_one_network():

    assert invert_networks_dict(mult_p_one_n) == {'A': ['apple', 'animal']}


def test_mult_person_mult_network():

    assert invert_networks_dict(mult_p_mult_n) == \
    {'a': ['apple'], 'A': ['apple', 'animal'], 'b': ['bike'], 'B': ['bike']}


def test_one_person_no_network():

    assert invert_networks_dict(one_p_zero_n) == {}


def test_mult_person_no_network():

    assert invert_networks_dict(mult_p_zero_n) == {}


if __name__ == '__main__':
    nose.runmodule()
