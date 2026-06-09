class TreeNode:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

    @staticmethod
    def parse_tuple(data):
        if isinstance(data, tuple) and len(data) == 3:
            key, value = data[1]
            node = TreeNode(key, value)
            node.left = TreeNode.parse_tuple(data[0])
            node.right = TreeNode.parse_tuple(data[2])
            return node
        elif data is None:
            return None
        else:
            key, value = data
            return TreeNode(key, value)

    def display(node, show_details=False, space='\t', level=0):
        if node is None:
            print(space * level + '@')
            return
        if node.left is None and node.right is None:
            if show_details:
                print(space * level + f"{node.key} ({node.value})")
            else:
                print(space * level + str(node.key))
            return
        TreeNode.display(node.right, show_details, space, level + 1)
        if show_details:
            print(space * level + f"{node.key} ({node.value})")
        else:
            print(space * level + str(node.key))
        TreeNode.display(node.left, show_details, space, level + 1)

    def traverse_in_order(node, show_details=False):
        if node is None:
            return []
        if show_details:
            return TreeNode.traverse_in_order(node.left, show_details) + [(node.key, node.value)] + TreeNode.traverse_in_order(node.right, show_details)
        else:
            return TreeNode.traverse_in_order(node.left, show_details) + [node.key] + TreeNode.traverse_in_order(node.right, show_details)

    def tree_height(node):
        if node is None:
            return 0
        return 1 + max(TreeNode.tree_height(node.left), TreeNode.tree_height(node.right))

    def size(node):
        if node is None:
            return 0
        return 1 + TreeNode.size(node.left) + TreeNode.size(node.right)

    def remove_none(nums):
        return [x for x in nums if x is not None]

    def is_bst(node):
        if node is None:
            return True, None, None
        is_bst_l, min_l, max_l = TreeNode.is_bst_util(node.left)
        is_bst_r, min_r, max_r = TreeNode.is_bst_util(node.right)

        is_bst_node = (is_bst_l and is_bst_r and (max_l is None or node.key > max_l) and (min_r is None or node.key < min_r))
        min_key = min(TreeNode.remove_none([min_l, node.key, min_r]))
        max_key = max(TreeNode.remove_none([max_l, node.key, max_r]))

        return is_bst_node, min_key, max_key

    @staticmethod
    def is_bst_util(node):
        if node is None:
            return True, None, None
        is_bst_l, min_l, max_l = TreeNode.is_bst_util(node.left)
        is_bst_r, min_r, max_r = TreeNode.is_bst_util(node.right)

        is_bst_node = (is_bst_l and is_bst_r and (max_l is None or node.key > max_l) and (min_r is None or node.key < min_r))
        min_key = min(TreeNode.remove_none([min_l, node.key, min_r]))
        max_key = max(TreeNode.remove_none([max_l, node.key, max_r]))

        return is_bst_node, min_key, max_key

    def insert(self, key, value):
        if key < self.key:
            if self.left is None:
                self.left = TreeNode(key, value)
                self.left.parent = self
            else:
                self.left.insert(key, value)
        elif key > self.key:
            if self.right is None:
                self.right = TreeNode(key, value)
                self.right.parent = self
            else:
                self.right.insert(key, value)
        else:
            # Key already exists in the tree, handle according to specific requirements
            pass

    def update_value(self, key, new_value):
        if key < self.key:
            if self.left:
                self.left.update_value(key, new_value)
            else:
                print(f"Key {key} not found in the tree.")
        elif key > self.key:
            if self.right:
                self.right.update_value(key, new_value)
            else:
                print(f"Key {key} not found in the tree.")
        else:
            self.value = new_value
            print(f"Updated node with key {key} to new value {new_value}.")

# Test tree with insert and update
tree_data = (
    (('aakash', {'username': 'aakash01', 'name': 'Aakash Sharma', 'email': 'aakash@example.com'}),
     ('biraj', {'username': 'biraj01', 'name': 'Biraj Singh', 'email': 'biraj@example.com'}),
     ('hemanth', {'username': 'hemanth01', 'name': 'Hemanth Kumar', 'email': 'hemanth@example.com'})),
    ('jadhesh', {'username': 'jadhesh01', 'name': 'Jadhesh Verma', 'email': 'jadhesh@example.com'}),
    (('siddhant', {'username': 'siddhant01', 'name': 'Siddhant Roy', 'email': 'siddhant@example.com'}),
     ('sonaksh', {'username': 'sonaksh01', 'name': 'Sonaksh Patel', 'email': 'sonaksh@example.com'}),
     ('vishal', {'username': 'vishal01', 'name': 'Vishal Mehta', 'email': 'vishal@example.com'}))
)
tree = TreeNode.parse_tuple(tree_data)

# Display initial tree structure with keys only
print("Initial tree (keys only):")
TreeNode.display(tree, show_details=False, space='  ')

# Display initial tree structure with full details
print("\nInitial tree (full details):")
TreeNode.display(tree, show_details=True, space='  ')

# Insert new user
new_user = ('karthik', {'username': 'karthik01', 'name': 'Karthik G', 'email': 'karthik@example.com'})
tree.insert(new_user[0], new_user[1])

# Update existing user
tree.update_value('karthik', {'username': 'karthik01', 'name': 'Karthik G', 'email': 'karthik_new@example.com'})

# Display updated tree structure with keys only
print("\nTree after inserting and updating user (keys only):")
TreeNode.display(tree, show_details=False, space='  ')

# Display updated tree structure with full details
print("\nTree after inserting and updating user (full details):")
TreeNode.display(tree, show_details=True, space='  ')

# In-order traversal
print("In-order traversal (keys only):", TreeNode.traverse_in_order(tree, show_details=False))
print("In-order traversal (full details):", TreeNode.traverse_in_order(tree, show_details=True))
# Tree height
print("Tree height:", TreeNode.tree_height(tree))
# Tree size
print("Tree size:", TreeNode.size(tree))
# Is BST, Min key, Max key
is_bst, min_key, max_key = TreeNode.is_bst(tree)
print("Is BST:", is_bst)
print("Min key:", min_key)
print("Max key:", max_key)
