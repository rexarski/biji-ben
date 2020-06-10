import unittest
from tree import Tree


class TestContains(unittest.TestCase):
    def setUp(self):
        self.t1 = Tree(1)
        t2 = Tree(2)
        t3 = Tree(3)
        t4 = Tree(4)
        t5 = Tree(5)
        t6 = Tree(6)
        t3.add_subtrees([t4, t5])
        t2.add_subtrees([t6])
        self.t1.add_subtrees([t2, t3])
        # t1
        #     t2
        
        #           t6
        
        #     t3
        #           t4
        #           t5

    def test_typical_true_root(self):
        # Write a test that runs __contains__ on a typical tree,
        # where the item is in the tree, *at the root*
        self.assertTrue(self.t1.__contains__(1))

    def test_typical_true_nonroot(self):
        # Write a test that runs __contains__ on a typical tree,
        # where the item is in the tree, *not at the root*
        self.assertTrue(self.t1.__contains__(4))

    def test_typical_false(self):
        # Write a test that runs __contains__ on a typical tree,
        # where the item is not in the tree
        self.assertFalse(self.t1.__contains__(20))

    def test_empty(self):
        # Write a test to check the behaviour when you
        # call __contains__ on an empty tree
        t7 = Tree()
        self.assertTrue(not t7.__contains__(1))
        self.assertFalse(t7.__contains__(1))

class TestBranching(unittest.TestCase):
    def test_empty(self):
        t = Tree()
        self.assertEqual(t.get_branching_factor(), 0)
        

    def test_just_root(self):
        t = Tree(5)
        self.assertEqual(t.get_branching_factor(), 0)

    def test_just_children(self):
        t = Tree(2)
        t.add_subtrees([Tree(1), Tree(2), Tree('hi'), Tree([1])])
        self.assertEqual(t.get_branching_factor(), 4)

    def test_bigger(self):
        t = Tree(0)
        t1 = Tree(1)
        t2 = Tree(2)
        t3 = Tree(3)
        t4 = Tree(4)
        t.add_subtrees([t1, t2, t3])
        t1.add_subtrees([Tree(15), Tree(20), Tree(25)])
        t2.add_subtrees([t4])
        t4.add_subtrees([Tree(1), Tree(2)])
        t3.add_subtrees([])

        # Use assertAlmostEqual because we're comparing floats
        self.assertAlmostEqual(t.get_branching_factor(), 9/4)
        
class TestBranchingHelper(unittest.TestCase):
    def setUp(self):
        self.t1 = Tree(1)
        t2 = Tree(2)
        t3 = Tree(3)
        t4 = Tree(4)
        t5 = Tree(5)
        t6 = Tree(6)
        t3.add_subtrees([t4, t5])
        t2.add_subtrees([t6])
        self.t1.add_subtrees([t2, t3]) 
        
    def test_simple(self):
        self.assertEqual(self.t1.get_branching_factor_helper(),(5,3))

class TestInsert(unittest.TestCase):
    def setUp(self):
        self.t1 = Tree(1)
        t2 = Tree(2)
        t3 = Tree(3)
        t4 = Tree(4)
        t5 = Tree(5)
        t6 = Tree(6)
        t3.add_subtrees([t4, t5])
        t2.add_subtrees([t6])
        self.t1.add_subtrees([t2, t3])
    
    def test_simple(self):
        self.t1.insert(17)
        
if __name__ == '__main__':
    unittest.main(exit=False)
