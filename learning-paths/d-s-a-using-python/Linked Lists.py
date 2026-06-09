# Linked List 
# A linked list is a linear data structure where elements are stored in nodes, and each node points to the next node in the sequence.
# Unlike arrays, linked lists do not require contiguous memory allocation, allowing for efficient insertions and
# deletions. Each node typically contains a value and a reference (or pointer) to the next node in the list.
# replacement for the Dynamic Array class
#its a collection of nodes  
# it has a head and tail pointer
# for to do list , linked list is a good choice rather than dynamic array
# we can make stack and queue using linked list
# read functions are O(n) in linked list
# the time complexity of insertion and deletion is O(1) in linked list
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None






a=Node(10)
print(a) # Output: <__main__.Node object at 0x...> 
b=Node(20)
c=Node(30)
a.next = b  # Link the first node to the second node
b.next = c  # Link the second node to the third node
print(b.next)  # Output: <__main__.Node object at 0x...>
print(c.value)  # Output: 30

print(a.value) # Output: 10
print(a.next)  # Output: <__main__.Node object at 0x...>