# Dynamic Array
# Fun fact: list in python is a dynamic array
#This code is a simple implementation of a dynamic array in Python.# It allows you to add elements, remove elements, and access elements by index.
# It automatically resizes the underlying array when it runs out of space.
import ctypes

class Meralist:
    def __init__(self):
        # Initial capacity of the array (always >=1)
        self.size = 1
        # Number of actual elements stored
        self.n = 0
        # Allocate raw memory array of capacity 1
        self.array = self.make_array(self.size)

    def make_array(self, capacity):
        """
        Create a new low-level array with given capacity.
        """
        return (capacity * ctypes.py_object)()

    def resize(self, new_capacity):
        """
        Resize the underlying array to a new capacity.
        Copy over all elements from old array.
        """
        new_array = self.make_array(new_capacity)
        for i in range(self.n):
            new_array[i] = self.array[i]
        self.array = new_array
        self.size = new_capacity

    def __len__(self):
        """
        Return the number of elements in the array.
        """
        return self.n

    def __getitem__(self, index):
        """
        Get element at index.
        Raise IndexError if out of bounds.
        """
        if index < 0 or index >= self.n:
            raise IndexError("Index out of bounds")
        return self.array[index]

    def append(self, value):
        """
        Add a new element to the end of the array.
        If capacity is full, resize by doubling.
        """
        if self.n == self.size:
            self.resize(2 * self.size)
        self.array[self.n] = value
        self.n += 1

    def pop(self):
        """
        Remove and return the last element.
        If array becomes too sparse, shrink by half.
        """
        if self.n == 0:
            raise IndexError("Pop from empty array")
        value = self.array[self.n - 1]
        self.array[self.n - 1] = None
        self.n -= 1
        if self.n < self.size // 4:
            self.resize(max(self.size // 2, 1))
        return value

    def remove(self, value):
        """
        Remove the first occurrence of value.
        Shift subsequent elements left.
        Shrink if sparse.
        """
        for i in range(self.n):
            if self.array[i] == value:
                # Shift elements left
                for j in range(i, self.n - 1):
                    self.array[j] = self.array[j + 1]
                self.array[self.n - 1] = None
                self.n -= 1
                if self.n < self.size // 4:
                    self.resize(max(self.size // 2, 1))
                return
        raise ValueError("Value not found in array")
#

# indexing 
    def __getitem__(self, index):
        """
        Get element at index.
        Raise IndexError if out of bounds.
        """
        if index < 0 or index >= self.n:
            raise IndexError("Index out of bounds")
        return self.array[index]
    def __repr__(self):
        """
        String representation showing elements in list format.
        """
        return "[" + ", ".join(repr(self.array[i]) for i in range(self.n)) + "]"
# clear the array
    def clear(self):
        self.array = self.make_array(1)  # Reset to initial capacity
        self.size = 1
        self.n = 0
# find the index of an element
    def index(self,value):
        for i in range(self.n):
            if self.array[i] == value:
                return i
        raise ValueError("Value not found in array")

# insert an element at a specific index
    def insert(self,index,value):
        if index< 0 or index> self.n:
            raise IndexError("Index out of bounds")
        if self.n==self.size:
            self.resize(2*self.size)
        # Shift elements to the right
        for i in range(self.n, index, -1):
            self.array[i] = self.array[i - 1]
        self.array[index] = value
        self.n += 1
        if self.n < self.size // 4:
            self.resize(max(self.size // 2, 1))
# delete an element at a specific index
    def __delitem__(self, index):
        if index < 0 or index >= self.n:
            raise IndexError("Index out of bounds")
        # Shift elements to the left
        for i in range(index, self.n - 1):
            self.array[i] = self.array[i + 1]
        self.array[self.n - 1] = None
        self.n -= 1
        if self.n < self.size // 4:
            self.resize(max(self.size // 2, 1))
# Example usage of the Meralist class
# Create an instance of Meralist and perform some operations



list1 = Meralist()
print(list1.size)  # Initial capacity: 1
print(list1.n)     # Initial count: 0
print(list1)       # []

list1.append(10)
print(list1.size)  # Still capacity 1, will resize on next append

list1.append(20)
list1.append("Hello")
list1.append(True)
list1.append(3.14)
print(list1)       # [10, 20, 'Hello', True, 3.14]

list1.pop()
print(list1)       # [10, 20, 'Hello', True]

list1.remove("Hello")
print(list1)       # [10, 20, True]
list1.insert(1, "Inserted")
print(list1)       # [10, 'Inserted', 20, True]
list1.__delitem__(2)
print(list1)       # [10, 'Inserted', True]
list1.clear()
print(list1)       # []
