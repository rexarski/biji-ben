class EmptyValue:
    pass

class LinkedListRec:
    
    def __init__(self, items):
        if len(items) == 0:
            self.first = EmptyValue
            self.rest = None
        else:
            self.first = items[0]
            self.rest = LinkedListRec(items[1:])
            
    def is_empty(self):
        return self.first is EmptyValue
    
    #1. NON-MUTATING
    
    #1.1 Find the size of the list.
    def size(self):
        length = 0        
        if self.is_empty():
            return 0
        else:
            length += 1
            return length + self.rest.size()
    
    #1.2 Find the number of times the item 6 occurs in the list.
    def six_appear(self):
        count = 0
        if self.is_empty():
            return 0
        else:
            if self.first == 6:
                count += 1
            return self.rest.six_appear() + count
    
    #1.3 Find the number of times a given item occurs in the list.
    def n_appear(self, n):
        count = 0
        if self.is_empty():
            return 0
        else:
            if self.first == n:
                count += 1
            return self.rest.n_appear(7) + count
    
    #1.4 Find the sum of the numbers in the list.
    def sum_up(self):
        sum = 0
        if self.is_empty():
            return 0
        else:
            sum += self.first
            return sum + self.rest.sum_up()
    
    #1.5 Find out if there is a repeated item in the list.
    def repeat(self, clipboard=[]):
        if self.is_empty():
            return False
        else:
            if self.first in clipboard:
                return True
            else:
                clipboard.append(self.first)
                return self.rest.repeat(clipboard)

    #1.6 Count the number of even items in the list.
    def even_num(self):
        if self.is_empty():
            return 0
        else:
            if self.first % 2 == 0:
                even = 1
            else:
                even = 0
            return even + self.rest.even_num()
        
    #1.7 Return a list containing all duplicate items in the list.
    def duplicates(self, clipboard=[], dup=[]):
        if self.is_empty():
            return dup
        else:
            if self.first in clipboard:
                dup += [self.first]
            clipboard.append(self.first)
            return self.rest.duplicates(clipboard, dup)
            
    #1.8 Return the number of items two lists have in common.
    def common(self, other):
        num = 0
        clip = other.llr_copy()
        if self.is_empty():
            return num
        else:
            if self.first in clip:
                num += 1
            return num + self.rest.common(other)
    
    def llr_copy(self, l=[]):
        if self.is_empty():
            return l
        else:
            l.append(self.first)
            return self.rest.llr_copy(l)
            
    #1.9 Implement "merge" on two sorted linked lists. Return a new linked list.
    #def merge(self, other):
        #new = []
        #if self.is_empty() and other.is_empty():
            #return LinkedListRec(new)
        #else:
            #if self.is_empty():
                #new.append(other.first)
                #self.merge(other.rest)
            #elif other.is_empty():
                #new.append(self.first)
                #self.rest.merge(other)
            #else:
                #if self.first <= other.first:
                    #new.append(self.first)
                    #self.rest.merge(other)
                #else: #self.first > other.first
                    #new.append(other.first)
                    #self.merge(other.rest)
    
    #2. MUTATING
    
    #2.1 Remove the first item from the list.
    def remove_first(self):
        if self.is_empty():
            raise IndexError
        else:
            self.first = self.rest.first
            self.rest = self.rest.rest
        
    #2.2 Remove the i-th item from the list (i is a parameter).
    def __len__(self):
        if self.is_empty():
            return 0
        else:
            return self.rest.__len__() + 1
        
    def remove(self, index):
        if self.is_empty():
            raise IndexError
        elif self.__len__() - 1 < index:
            raise IndexError
        elif index == 0:
            self.remove_first()
        else:
            self.rest.remove(index - 1)
            
    #2.3 Remove all even items from the list.
    def remove_even(self):
        if self.is_empty():
            return self
        else:
            if self.first % 2 == 0:
                self.remove_first()
                self.rest.remove_even()
            else:
                self.rest.remove_even()
    
    #2.4 Insert an item at the front of the list.
    def insert_first(self, item):
        temp = LinkedListRec([])
        temp.first = self.first
        temp.rest = self.rest
        self.first = item
        self.rest =temp
        
    #2.5 Insert an item at the back of the list.
    def insert_last(self, item):
        self.insert(len(self), item)
    
    #2.6 Insert an item at the i-th position in the list.
    def insert(self, index, item):
        if index > len(self):
            raise IndexError
        elif index == 0:
            self.insert_first(item)
        else:
            self.rest.insert(index - 1, item)

    #2.7 Remove all duplicates from the list.
    def remove_dup(self):
        dup = self.duplicates()
        if self.is_empty():
            return self
        else:
            if self.first in dup:
                self.remove_first()
                self.rest.remove_dup()
            else:
                self.rest.remove_dup()

    #2.8 Take two lists, and contatenate the second to the end of the first.
    def contatenate(self, other):
        if self.is_empty():
            return other
        elif other.is_empty():
            return self
        else:
            self.insert_last(other.first)
            self.contatenate(other.rest)
    
    #2.9 Remove the first n items from the list.
    def remove_first_n(self, n):
        if n > len(self):
            raise IndexError
        elif n == 1:
            return self.remove_first()
        else:
            self.first = self.rest.first
            self.rest = self.rest.rest
            self.remove_first_n(n - 1)
    
    #2.10 Remove the last n items from the list.
    def remove_last_n(self, n):
        m = len(self) - n
        self.remove_first_n(m)
    
    #2.11 Remove all items after the first occurrence of 1 from the list.    
    def remove_all_after_first_occurence(self):
        if self.is_empty():
            pass
        else:
            if self.first == 1:
                self.rest = None
            else:
                self.rest.remove_all_after_first_occurence()