# encode x1 + x2 + ... + xn >= k using sequential encoding

g_n: int
g_k: int
g_offset: int

# 1 -> n: xi

# xi => ri1


def constraint_1():
    c = []
    for i in range(1, g_n+1):
        c.append([-get_x(i), get_r(i, 1)])
        if i <= g_k:
            c.append([get_x(i), get_r(i, i)])
    return c

# -rij


def constraint_2():
    c = []
    for i in range(1, g_k):
        for j in range(i+1, g_k+1):
            c.append([-get_r(i, j)])
    return c

# ri-1,j => rij


def constraint_3():
    c = []
    for i in range(2, g_n+1):
        for j in range(1, g_k+1):
            c.append([-get_r(i-1, j), get_r(i, j)])
    return c

# xi ^ ri-1,j-1 => rij
# -xi ^ -ri-1,j => -rij
# -ri-1,j ^ -ri-1,j-1 => -rij


def constraint_4():
    c = []
    for i in range(2, g_n+1):
        for j in range(1, g_k+1):
            if j > 1:
                c.append([-get_x(i), -get_r(i-1, j-1), get_r(i, j)])
                c.append([get_r(i-1, j), get_r(i-1, j-1), -get_r(i, j)])
            c.append([get_x(i), get_r(i-1, j), -get_r(i, j)])
    return c


# rn-1,k v (xn ^ rn-1,k-1) (5.1)
# -xn => rn-1,k (5.2)
# -xi ^ rik => ri-1,k for i > k (5.3)
def constraint_5():
    c = []
    # 5.1
    c.append([get_r(g_n-1, g_k), get_x(g_n)])
    c.append([get_r(g_n-1, g_k), get_r(g_n-1, g_k-1)])
    # 5.2
    c.append([get_x(g_n), get_r(g_n-1, g_k)])
    # 5.3
    for i in range(g_k+1, g_n+1):
        c.append([get_x(i), -get_r(i, g_k), get_r(i-1, g_k)])
    return c


def at_least_k(n, k, offset):
    """
        Create clause for constraint: At least k variables in a set of given n variables are True

        Args:
            k (int): The number of variables must be True
            n (int): The number of given variables
            offset (int): The offset of variables compared to 1
    """
    global g_n, g_k, g_offset
    g_n = n
    g_k = k
    g_offset = offset
    clauses = []
    clauses.extend(constraint_1())
    clauses.extend(constraint_2())
    clauses.extend(constraint_3())
    clauses.extend(constraint_4())
    clauses.extend(constraint_5())
    return clauses


def get_r(i, j):
    return g_n+(i-1)*g_k+j+g_offset


def get_x(i):
    return i+g_offset
