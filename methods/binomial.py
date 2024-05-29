def at_least_k(n, k, offset):
    """
        Create clause for constraint: At least k variables in a set of given n variables are True
        
        Args:
            k (int): The number of variables must be True
            n (int): The number of given variables
            offset (int): The offset of variables compared to 1
    """
    def backtrack(start, combination):
        if len(combination) == combination_length:
            combinations_list.append(combination[:])
            return
        for i in range(start, n + 1):
            combination.append(i + offset)
            backtrack(i + 1, combination)
            combination.pop()
    combination_length = n - k + 1
    combinations_list = []
    backtrack(1, [])
    return combinations_list