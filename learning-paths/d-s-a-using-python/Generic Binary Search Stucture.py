def binary_search(lo, hi, condition):
    # Keep looping as long as the search space is valid
    while lo <= hi:
        # Find the midpoint index
        mid = (lo + hi) // 2
        # Evaluate the condition function for this mid index
        result = condition(mid)

        # If the condition reports "found", return the mid index
        if result == "found":
            return mid
        # If the target is in the left half, adjust hi
        elif result == "left":
            hi = mid - 1
        # Otherwise, the target is in the right half, adjust lo
        else:
            lo = mid + 1

    # If we exit the loop, the target was not found
    return "Not found"


# Example usage with decreasing order list
cards = [13, 11, 5, 4, 10, 7, 4, 3, 1, 0]
query = 10

# The lambda function determines where to search next:
# - If cards[mid] == query, we found it.
# - If cards[mid] > query, the target is to the right (since decreasing).
# - Otherwise, the target is to the left.
result = binary_search(
    0, 
    len(cards) - 1, 
    lambda mid: (
        "found" if cards[mid] == query 
        else "left" if cards[mid] > query 
        else "right"
    )
)

print("Card found at index:", result)
# Output: Card found at index: 4
# If the target number is not found, the function should return "Not found".