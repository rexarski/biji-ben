import nose
import insert

def test_empty():
    L = []
    insert.insert_after(L, 1, 1) 
    assert L == [], "insert_after([], 1, 1) should leave\n" + \
           "L = %s not %s" % ([], L)
    
def test_one_not_n1():
    L = [0]
    insert.insert_after(L, 4, 99)
    assert L == [0], "insert_after([0], 4, 99) should change L to %s, " + \
           "but L is %s" % ([0], L)
    
def test_one_n1():
    L = [0]
    insert.insert_after(L, 0, 99)
    assert L == [0, 99], "insert_after([0], 0, 99) should change L to %s," \
           "but L is %s" % ([0, 99], L)
    
def test_longer_no_n1():
    L = [0, 1, 2, 3, 4, 5]
    insert.insert_after(L, 14, 99)
    assert L == [0, 1, 2, 3, 4, 5], "L longer, no n1"
    
def test_longer_n1_front():
    L = [0, 1, 2, 3, 4, 5]
    insert.insert_after(L, 0, 99)
    assert L == [0, 99, 1, 2, 3, 4, 5], "L longer, n1 at front"
    
def test_longer_n1_end():
    L = [0, 1, 2, 3, 4, 5]
    insert.insert_after(L, 5, 99)
    assert L == [0, 1, 2, 3, 4, 5, 99], "L longer n1 at end"
    
def test_longer_n1_middle():
    L = [0, 1, 2, 3, 4, 5]
    insert.insert_after(L, 2, 99)
    assert L == [0, 1, 2, 99, 3, 4, 5], "L longer, n1 in middle"
    
def test_longer_n1_several():
    L = [0, 1, 2, 3, 4, 2, 5, 2]
    insert.insert_after(L, 2, 99)
    assert L == [0, 1, 2, 99, 3, 4, 2, 99, 5, 2, 99], \
           "L longer, several n1s, separate"
    
def test_n1_equals_n2():
    L = [0, 1, 2, 3, 4, 2, 5, 2]
    insert.insert_after(L, 2, 2)
    assert L == [0, 1, 2, 2, 3, 4, 2, 2, 5, 2, 2], \
           "n1 equals n2"
           
if __name__ == "__main__":
    nose.runmodule()