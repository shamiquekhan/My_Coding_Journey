class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node

    def display(self):
        curr = self.head
        while curr:
            print(curr.data, end=" -> ")
            curr = curr.next
        print('None')

    # Recursive helper to find max node
    def find_max_node(self, node, max_node):
        if node is None:
            return max_node
        if max_node is None or node.data > max_node.data:
            max_node = node
        return self.find_max_node(node.next, max_node)

    # Replace max value with a given value
    def replace_max_recursive(self, new_value):
        max_node = self.find_max_node(self.head, None)
        if max_node:
            old = max_node.data
            max_node.data = new_value
            print(f"Max value {old} replaced with {new_value}")
        else:
            print("List is empty, no max value to replace.")

    # New: Recursive sum of odd numbers
    def sum_of_odds_recursive(self, node=None):
       temp=self.head
       counter = 0
       result = 0
       while temp is not None:
           if temp.data % 2 != 0:
               result += temp.data
           temp = temp.next
       return result
    def reverse(self):
        prev_node = None
        curr_node = self.head
        while curr_node is not None:
            next_node = curr_node.next
            curr_node.next = prev_node
            prev_node = curr_node
            curr_node = next_node
        self.head = prev_node
        return self.head


# Example usage
ll = LinkedList()
for val in [3, 12, 5, 8, 7]:
    ll.append(val)

print("Original List:")
ll.display()

# Replace max value with 100
ll.replace_max_recursive(100)
print("Updated List:")
ll.display()

# Sum of odd numbers
odd_sum = ll.sum_of_odds_recursive()
print("Sum of all odd numbers:", odd_sum)

# Reverse the list
ll.reverse()
print("Reversed List:")
ll.display()

