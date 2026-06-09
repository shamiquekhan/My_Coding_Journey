# insert Linked List
# Inserting at the beginning 
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        # self.head = None  # already assigned above; no need to repeat
        self.n = 0  # not used, can be removed or used for node count
        self.size = 0  # used to track list size
        self.tail = None  # not used, could be useful for O(1) append

    def insert_at_beginning(self, value):
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node
        self.size += 1  # increment size

    # to traverse the linked list and return a string representation
    # of the values in the nodes
    def __str__(self):
        if self.head is None:
            return "Empty List"
        curr = self.head
        result = ""
        while curr is not None:
            result += str(curr.data) + " -> "
            curr = curr.next
        return result[:-4]  # remove trailing ' -> '

# insert from tail (append)
    def append(self, value):
        new_node = Node(value)
        # If the list is empty, set the new node as the head
        if self.head is None:
            self.head = new_node
            self.size += 1
            return
        # Traverse to the end of the list
        curr = self.head
        while curr.next is not None:
            curr = curr.next
        curr.next = new_node
        self.size += 1  # increment size

# insert at middle (anywhere in the list)
    def insert_after(self, after, value):
        new_node = Node(value)
        curr = self.head
        while curr is not None:
            if curr.data == after:
                break
            curr = curr.next
        # case 1 = YOU broke the loop
        # case 2 loop run completely i.e. curr = None
        if curr is not None:
            new_node.next = curr.next
            curr.next = new_node
            self.size += 1
            # print(curr.data)
        else:
            print("Item not found")

# deletion 
# clear function (make the list empty)
    def clear(self):
        self.head = None
        self.size = 0

# delete from the head
    def del_head(self):
        if self.head is None:
            print("Empty list")
        else:
            self.head = self.head.next
            self.size -= 1

# delete from the tail - Pop function
    def pop(self):
        curr = self.head
        if curr is None:
            print("List is empty")
            return
        if curr.next is None:
            self.clear()
            return
        while curr.next.next is not None:
            curr = curr.next
        # curr = second last item
        curr.next = None
        self.size -= 1

# delete by value 
    def del_value(self, value):
        if self.head is None:
            return 'not found'
        if self.head.data == value:
            self.head = self.head.next
            self.size -= 1
            return

        curr = self.head
        while curr.next is not None:
            if curr.next.data == value:
                break
            curr = curr.next
        # case 1 : we got the item 
        # case 2 : we didn’t get the item 
        if curr.next is None:
            return 'not found'
        else:
            curr.next = curr.next.next
            self.size -= 1
# search 
#search by value (find)
    def search(self,value):
        curr=self.head
        pos=0
        while curr != None:
            if curr.data == value:
                return pos
            curr=curr.next
            pos=pos +1
        return 'not found' 
#search by index 
    def search_index(self,index):
        curr=self.head
        pos=0
        while curr !=None:
            if pos==index:
                return curr.data
            curr=curr.next
            pos+=1
        return 'Index Error'
#delete by index
    def del_at_index(self, index):
        if index < 0 or index >= self.size:
            print("Invalid index")
            return

        if index == 0:
            self.head = self.head.next
            self.size -= 1
            return

        curr = self.head
        for i in range(index - 1):  # go to (index-1)th node
            curr = curr.next

    # curr is now before the node to delete
        curr.next = curr.next.next
        self.size -= 1

    




# example usage
if __name__ == "__main__":
    ll = LinkedList()
    ll.insert_at_beginning(10)
    ll.insert_at_beginning(20)
    ll.insert_at_beginning(30)
    print(ll)  # Output: 30 -> 20 -> 10

    ll.append(40)
    print(ll)  # Output: 30 -> 20 -> 10 -> 40
    ll.search(40)
    ll.search_index(0)
    ll.insert_after(20, 25)
    ll.insert_after(2, 25)  # should print "Item not found"

    ll.del_value(30)
    print(ll)  # Output should not include 30

    ll.del_head()
    print(ll)

    ll.pop()
    ll.pop()
    print(ll)

    ll.pop()
    print(ll)

    ll.clear()
    print(ll)






