#lec08

midterm will cover up till this lecture.
October 1, 2014

	curry = self.first
	while cure is not None:
		curr = curr.next
	

when we do a removal to a linked list, first we navigate to the index that we desire to remove:

- remove it, by writing curr = curr.next
- then update the link, curr.next = curr.next.next

we need to change the 'next' attribute of node (index - 1) from pointing to node (index) to node (index + 1)

go to node (index-1)

	curr = self.first
	for i in range(index - 1):
		curr = curr.next
	curr.next = curr.next.next

