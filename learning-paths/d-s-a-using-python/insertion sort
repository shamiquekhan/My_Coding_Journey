def insertion_sort(nums):
    nums = list(nums)  # Copying the input list to avoid mutating it
    for i in range(1, len(nums)):  # Start from the second element
        cur = nums[i]
        j = i - 1
        while j >= 0 and nums[j] > cur:
            nums[j + 1] = nums[j]  # Shift element to the right
            j -= 1
        nums[j + 1] = cur  # Place the current element in its correct position
    return nums

# Example test case
test0 = {
    'input': {'nums': [5, 2, 9, 1, 5, 6]},
    'output': [1, 2, 5, 5, 6, 9]
}

nums0, output0 = test0['input']['nums'], test0['output']
print('input', nums0)
print('expected output', output0)
result0 = insertion_sort(nums0)
print('actual output', result0)
print('match : ', result0 == output0)
