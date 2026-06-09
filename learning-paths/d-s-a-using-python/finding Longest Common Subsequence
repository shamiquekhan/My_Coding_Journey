def longest_common_subsequence(word1, word2):
    m, n = len(word1), len(word2)
    # if m==len(word1) or n==len(word2):
    #     return 0
    # Create a 2D table to store lengths of longest common subsequence.
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Build the table in bottom-up fashion.
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Reconstruct the longest common subsequence from the dp table.
    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if word1[i - 1] == word2[j - 1]:
            lcs.append(word1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    # The lcs list will contain the LCS in reverse order.
    lcs.reverse()
    return ''.join(lcs)

# Example usage:
word1 = "sqazwsxedcrfvtgbyhnujmikolp"
word2 = "plmokmijnqazwsxedcrfvtgbyhnujm"
print(f"The longest common subsequence between '{word1}' and '{word2}' is '{longest_common_subsequence(word1, word2)}'")

