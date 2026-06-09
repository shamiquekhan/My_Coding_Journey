def merge(left, right):
    sorted_nums = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            sorted_nums.append(left[i])
            i += 1
        else:
            sorted_nums.append(right[j])
            j += 1
    # Append remaining elements, if any
    while i < len(left):
        sorted_nums.append(left[i])
        i += 1
    while j < len(right):
        sorted_nums.append(right[j])
        j += 1
    return sorted_nums

def merge_sort(nums):
    if len(nums) <= 1:
        return nums
    mid = len(nums) // 2
    left = nums[:mid]
    right = nums[mid:]
    left_sorted = merge_sort(left)
    right_sorted = merge_sort(right)
    sorted_nums = merge(left_sorted, right_sorted)
    return sorted_nums

# Example test case
test0 = {
    'input': {'nums': [5, 2, 9, 1, 5, 6]},
    'output': [1, 2, 5, 5, 6, 9]
}

nums0, output0 = test0['input']['nums'], test0['output']
print('input', nums0)
print('expected output', output0)
result0 = merge_sort(nums0)
print('actual output', result0)
print('match : ', result0 == output0)
