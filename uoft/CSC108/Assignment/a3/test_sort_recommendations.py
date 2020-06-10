import nose
from a3_functions import sort_recommendations

lst1 = [('Steve Jobs', 10), ('Bill Gates', 10), ('Larry Page', 10)]
lst2 = [('Steve Jobs', 8), ('Bill Gates', 9), ('Larry Page', 10)]
lst3 = []
lst4 = [('Jen Campbell', 100)]


def test_same_score():
    '''Test the case that different potential friends have same score.'''

    assert sort_recommendations(lst1) == ['Bill Gates', 'Larry Page', \
    'Steve Jobs']


def test_different_score():
    '''Test the case that different potential friends have different scores.'''

    assert sort_recommendations(lst2) == ['Larry Page', 'Bill Gates', \
    'Steve Jobs']


def test_empty_recommendation():
    '''Test the case which has nothing in the list.'''

    assert sort_recommendations(lst3) == []


def test_single_person():
    '''Test the case which has only one person in the list.'''

    assert sort_recommendations(lst4) == ['Jen Campbell']


if __name__ == '__main__':
    nose.runmodule()
