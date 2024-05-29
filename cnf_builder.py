import methods.new_sequential_encoding as nse
import methods.old_sequential_encoding as ose
import methods.binomial as binomial
import helper
import math

g_num_items: int
g_num_transactions: int
g_min_support: int
g_mode: int
g_clauses = []

# q1 ↔ ¬p1 ^ ¬p2 ^ ¬p3
# expect: ((¬q1 | ¬p1) & (¬q1 | ¬p2) & (¬q1 | ¬p3) & (q1 | p1 | p2 | p3))
def build_cnf_for_each_transaction(items, transaction_idx):
    global g_clauses
    indice_q = g_num_items + transaction_idx
    neg_items = [item for item in items if item % 2 == 0]
    # constaint (5)
    c_5 = [[-indice_q, -int(item/2+1)] for item in neg_items]
    g_clauses.extend(c_5)
    # constaint (6)
    c_6 = [int(item/2+1) for item in neg_items]
    c_6.extend([indice_q])
    g_clauses.append(c_6)

def additional_constraints():
    global g_clauses
    # at least 1 item in set
    c = [i for i in range(1,g_num_items+1)]
    g_clauses.append(c)

def at_least_k():
    global g_clauses
    clause = binomial.at_least_k(g_num_transactions, g_min_support, g_num_items)
    g_clauses.extend(clause)

def at_least_k_se():
    global g_clauses
    clause = nse.at_least_k(g_num_transactions, g_min_support, g_num_items)
    g_clauses.extend(clause)

def at_least_k_old_se():
    global g_clauses
    clause = ose.constraints(g_num_transactions, g_min_support, g_num_items)
    g_clauses.extend(clause)

def process_file(input_file):
    with open(input_file) as f:
        if g_mode == 1:
            at_least_k()
        elif g_mode == 2:
            at_least_k_se()
        elif g_mode == 3:
            at_least_k_old_se()
        else:
            raise ValueError("Encoding mode {} is not implemented".format(g_mode))
        additional_constraints()
        for i, line in enumerate(f):
            # Split the line into individual values
            transaction_idx = i + 1
            values = line.strip().split()
            values = [int(value) for value in values]
            build_cnf_for_each_transaction(values, transaction_idx)
            

def read_params(input_file):
    global g_num_items, g_num_transactions, g_min_support
    with open(input_file) as f:
        lines = f.readlines()
        g_num_transactions = len(lines)
        g_num_items = int(max([int(value) for value in [int(value) for line in lines for value in line.strip().split()]])/2 + 1)

def run(input_file, output_file, min_supp, mode):
    global g_min_support, g_mode, g_clauses, g_num_items, g_num_transactions
    g_mode = mode
    g_clauses.clear()
    read_params(input_file)
    if 0 < min_supp < 1:
        g_min_support = int(math.ceil(min_supp * g_num_transactions))
    else:
        g_min_support = int(math.ceil(min_supp))
    process_file(input_file)
    n_vars = helper.get_max_item(g_clauses)
    helper.write_cnf_to_file(n_vars, g_clauses, output_file)
    return g_num_items, g_num_transactions, n_vars, len(g_clauses)
