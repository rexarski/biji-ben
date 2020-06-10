class Node:
    def __init__(self, cargo=None, next=None):
        self.cargo = cargo
        self.next = next
        
    def __str__(self):
        return str(self.cargo)
    
    def print_list(node):
        while node is not None:
            print (node, end=' ')
            node = node.next
        print()